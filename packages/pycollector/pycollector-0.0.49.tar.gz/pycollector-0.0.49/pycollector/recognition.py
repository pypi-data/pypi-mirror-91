import os
import sys
import torch
import vipy
import shutil
import numpy as np
from vipy.util import remkdir, filetail, readlist, tolist, filepath
from datetime import datetime
from pycollector.video import Video
from pycollector.model.yolov3.network import Darknet
from pycollector.globals import print
from pycollector.model.pyvideoresearch.bases.resnet50_3d import ResNet503D, ResNet3D, Bottleneck3D
import pycollector.model.ResNets_3D_PyTorch.resnet
import pycollector.label
import pycollector.dataset
import vipy.activity
import itertools
import copy
import os
import torch
from torch import nn
import torch.nn.functional as F
from torchvision.datasets import MNIST
import torch.utils.data
from torch.utils.data import DataLoader, random_split, Dataset
from torchvision import transforms
import pytorch_lightning as pl
import json
import math


class ActivityRecognition(object):
    def __init__(self, pretrained=True):
        self.net =  None
        self._class_to_index = {}
        self._num_frames = 0

    def class_to_index(self, c=None):
        return self._class_to_index if c is None else self._class_to_index[c]
    
    def index_to_class(self, index=None):
        d = {v:k for (k,v) in self.class_to_index().items()}
        return d if index is None else d[index]
    
    def classlist(self):
        return [k for (k,v) in sorted(list(self.class_to_index().items()), key=lambda x: x[0])]  # sorted in index order

    def num_classes(self):
        return len(self.classlist())

    def fromindex(self, k):
        index_to_class = {v:k for (k,v) in self.class_to_index().items()}
        assert k in index_to_class, "Invalid class index '%s'" % (str(k))
        return index_to_class[k]

    def label_confidence(self, video=None, tensor=None, threshold=None):
        raise
        logits = self.__call__(video, tensor)
        conf = [[(self.index_to_class(j), s[j]) for j in i[::-1] if threshold is None or s[j]>threshold] for (s,i) in zip(logits, np.argsort(logits, axis=1))]
        return conf if len(logits) > 1 else conf[0]

    def activity(self, video, threshold=None):
        (c,s) = zip(*self.label_confidence(video=video, threshold=None))
        return vipy.activity.Activity(startframe=0, endframe=self._num_frames, category=c[0], actorid=video.actorid(), confidence=s[0]) if (threshold is None or s[0]>threshold) else None
            
    def top1(self, video=None, tensor=None, threshold=None):
        raise
        return self.topk(k=1, video=video, tensor=tensor, threshold=threshold)

    def topk(self, k, video=None, tensor=None, threshold=None):
        raise
        logits = self.__call__(video, tensor)
        topk = [[self.index_to_class(j) for j in i[-k:][::-1] if threshold is None or s[j] >= threshold] for (s,i) in zip(logits, np.argsort(logits, axis=1))]
        return topk if len(topk) > 1 else topk[0]

    def temporal_support(self):
        return self._num_frames

    def totensor(self, training=False):
        raise

    def binary_vector(self, categories):
        y = np.zeros(len(self.classlist())).astype(np.float32)
        for c in tolist(categories):
            y[self.class_to_index(c)] = 1
        return torch.from_numpy(y).type(torch.FloatTensor)
        
    
    
class PIP_250k(pl.LightningModule, ActivityRecognition):
    """Activity recognition using people in public - 250k stabilized"""
    
    def __init__(self, pretrained=True, deterministic=False, modelfile=None, mlbl=False, mlfl=False):
        super().__init__()
        self._input_size = 112
        self._num_frames = 16        
        self._mean = [0.485, 0.456, 0.406]
        self._std = [0.229, 0.224, 0.225]
        self._mlfl = mlfl
        self._mlbl = mlbl

        if deterministic:
            np.random.seed(42)

        #self._class_to_weight = {'car_drops_off_person': 0.5415580813018052, 'car_picks_up_person': 0.5166285035486872, 'car_reverses': 0.4864531915292076, 'car_starts': 0.4373510029809646, 'car_stops': 0.2710265819171847, 'car_turns_left': 0.8712633574636675, 'car_turns_right': 0.3827979879057864, 'hand_interacts_with_person_highfive': 1.4962896036348539, 'person': 0.08372274235167537, 'person_abandons_object': 0.5294114478840813, 'person_carries_heavy_object': 0.3982262588212442, 'person_closes_car_door': 0.30026000397668684, 'person_closes_car_trunk': 0.6329073059937789, 'person_closes_facility_door': 0.3572828721142877, 'person_embraces_person': 0.321974093136734, 'person_enters_car': 0.30481062242606516, 'person_enters_scene_through_structure': 0.31850059486555565, 'person_exits_car': 0.4071776409464214, 'person_exits_scene_through_structure': 0.38887859050533025, 'person_holds_hand': 0.37311850556431675, 'person_interacts_with_laptop': 0.5288033409750182, 'person_loads_car': 1.217126295244549, 'person_opens_car_door': 0.24504116978076299, 'person_opens_car_trunk': 1.0934851888105013, 'person_opens_facility_door': 0.4955138087004537, 'person_picks_up_object_from_floor': 1.1865967553059953, 'person_picks_up_object_from_table': 3.9581702614257934, 'person_purchases_from_cashier': 3.795407604809639, 'person_purchases_from_machine': 3.013281383565209, 'person_puts_down_object_on_floor': 0.5693359450623614, 'person_puts_down_object_on_shelf': 8.586138553443124, 'person_puts_down_object_on_table': 2.2724770752049683, 'person_reads_document': 0.3950204136071002, 'person_rides_bicycle': 1.120112034972008, 'person_shakes_hand': 0.7939816984366945, 'person_sits_down': 0.475769278518198, 'person_stands_up': 0.9511469708058823, 'person_steals_object_from_person': 0.6749376770458883, 'person_talks_on_phone': 0.1437150138699926, 'person_talks_to_person': 0.12953931093794052, 'person_texts_on_phone': 0.34688865531083296, 'person_transfers_object_to_car': 2.2351615915353835, 'person_transfers_object_to_person': 0.6839705972370579, 'person_unloads_car': 0.6080991393803349, 'vehicle': 0.060641247145963084}

        self._class_to_weight = {'car_drops_off_person': 1.4162811344926518, 'car_picks_up_person': 1.4103618337303332, 'car_reverses': 1.0847976470131024, 'car_starts': 1.0145749063037774, 'car_stops': 0.6659236295324015, 'car_turns_left': 2.942269221156227, 'car_turns_right': 1.1077783089040996, 'hand_interacts_with_person_highfive': 2.793646013249904, 'person': 0.4492053391155403, 'person_abandons_object': 1.0944029463871692, 'person_carries_heavy_object': 0.5848339202761978, 'person_closes_car_door': 0.8616907697519004, 'person_closes_car_trunk': 1.468393359799126, 'person_closes_facility_door': 0.8927495923340439, 'person_embraces_person': 0.6072654081071569, 'person_enters_car': 1.3259274145537951, 'person_enters_scene_through_structure': 0.6928103470838287, 'person_exits_car': 1.6366577285051707, 'person_exits_scene_through_structure': 0.8368692178634396, 'person_holds_hand': 1.2378881634203558, 'person_interacts_with_laptop': 1.6276031281396193, 'person_loads_car': 2.170167410167583, 'person_opens_car_door': 0.7601817241565009, 'person_opens_car_trunk': 1.7255285914206204, 'person_opens_facility_door': 0.9167411017455822, 'person_picks_up_object_from_floor': 1.123251610875369, 'person_picks_up_object_from_table': 3.5979689180114205, 'person_purchases_from_cashier': 7.144918373837205, 'person_purchases_from_machine': 5.920886403645001, 'person_puts_down_object_on_floor': 0.7295795950752353, 'person_puts_down_object_on_shelf': 9.247614426653692, 'person_puts_down_object_on_table': 1.9884672074906158, 'person_reads_document': 0.7940480628992879, 'person_rides_bicycle': 2.662661823600623, 'person_shakes_hand': 0.7819547332927879, 'person_sits_down': 0.8375202893491961, 'person_stands_up': 1.0285510019795079, 'person_steals_object_from_person': 1.0673909796893626, 'person_talks_on_phone': 0.3031855242664589, 'person_talks_to_person': 0.334895684562076, 'person_texts_on_phone': 0.713951043919232, 'person_transfers_object_to_car': 3.2832615561297605, 'person_transfers_object_to_person': 0.9633429807282274, 'person_unloads_car': 1.1051597100801462, 'vehicle': 1.1953172363332243}
        self._class_to_weight['person_puts_down_object_on_shelf'] = 1.0   # run 5

        self._class_to_index = {'car_drops_off_person': 0, 'car_picks_up_person': 1, 'car_reverses': 2, 'car_starts': 3, 'car_stops': 4, 'car_turns_left': 5, 'car_turns_right': 6, 'hand_interacts_with_person_highfive': 7, 'person': 8, 'person_abandons_object': 9, 'person_carries_heavy_object': 10, 'person_closes_car_door': 11, 'person_closes_car_trunk': 12, 'person_closes_facility_door': 13, 'person_embraces_person': 14, 'person_enters_car': 15, 'person_enters_scene_through_structure': 16, 'person_exits_car': 17, 'person_exits_scene_through_structure': 18, 'person_holds_hand': 19, 'person_interacts_with_laptop': 20, 'person_loads_car': 21, 'person_opens_car_door': 22, 'person_opens_car_trunk': 23, 'person_opens_facility_door': 24, 'person_picks_up_object_from_floor': 25, 'person_picks_up_object_from_table': 26, 'person_purchases_from_cashier': 27, 'person_purchases_from_machine': 28, 'person_puts_down_object_on_floor': 29, 'person_puts_down_object_on_shelf': 30, 'person_puts_down_object_on_table': 31, 'person_reads_document': 32, 'person_rides_bicycle': 33, 'person_shakes_hand': 34, 'person_sits_down': 35, 'person_stands_up': 36, 'person_steals_object_from_person': 37, 'person_talks_on_phone': 38, 'person_talks_to_person': 39, 'person_texts_on_phone': 40, 'person_transfers_object_to_car': 41, 'person_transfers_object_to_person': 42, 'person_unloads_car': 43, 'vehicle': 44}

        self._verb_to_noun = {k:set(['car','vehicle','motorcycle','bus','truck']) if (k.startswith('car') or k.startswith('motorcycle') or k.startswith('vehicle')) else set(['person']) for k in self.classlist()}

        self._class_to_shortlabel = pycollector.label.pip_to_shortlabel

        if pretrained:
            self._load_pretrained()
            self.net.fc = nn.Linear(self.net.fc.in_features, self.num_classes())
        elif modelfile is not None:
            self._load_trained(modelfile)
        
    def category(self, x):
        yh = self.forward(x if x.ndim == 5 else torch.unsqueeze(x, 0))
        return [self.index_to_class(int(k)) for (c,k) in zip(*torch.max(yh, dim=1))]

    def category_confidence(self, x):
        yh = self.forward(x if x.ndim == 5 else torch.unsqueeze(x, 0))
        return [(self.index_to_class(int(k)), float(c)) for (c,k) in zip(*torch.max(yh, dim=1))]

    def topk(self, x_logits, k):
        yh = x_logits.detach().cpu().numpy()
        topk = [[(self.index_to_class(j), s[j]) for j in i[-k:][::-1]] for (s,i) in zip(yh, np.argsort(yh, axis=1))]
        return topk

    def topk_probability(self, x_logits, k):
        yh = x_logits.detach().cpu().numpy()
        yh_prob = F.softmax(x_logits, dim=1).detach().cpu().numpy()
        topk = [[(self.index_to_class(j), c[j], p[j]) for j in i[-k:][::-1]] for (c,p,i) in zip(yh, yh_prob, np.argsort(yh, axis=1))]  
        return topk
        
    # ---- <LIGHTNING>
    def forward(self, x):
        return self.net(x)  # lighting handles device

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=1e-3)
        return optimizer

    def training_step(self, batch, batch_nb, logging=True, valstep=False):
        (x,Y) = batch  
        y_hat = self.forward(x)
        y_hat_softmax = F.softmax(y_hat, dim=1)

        (loss, n_valid) = (0, 0)
        C = torch.tensor([self._class_to_weight[k] for (k,v) in sorted(self._class_to_index.items(), key=lambda x: x[1])], device=y_hat.device)  # inverse class frequency        
        for (yh, yhs, labelstr) in zip(y_hat, y_hat_softmax, Y):
            labels = json.loads(labelstr)
            if labels is None:
                continue  # skip me
            lbllist = [l for lbl in labels for l in lbl]  # list of multi-labels within clip (unpack from JSON to use default collate_fn)
            lbl_frequency = vipy.util.countby(lbllist, lambda x: x)  # frequency within clip
            lbl_weight = {k:v/float(len(lbllist)) for (k,v) in lbl_frequency.items()}  # multi-label likelihood within clip, sums to one
            for (y,w) in lbl_weight.items():
                if valstep:
                    # Pick all labels normalized (https://papers.nips.cc/paper/2019/file/da647c549dde572c2c5edc4f5bef039c-Paper.pdf
                    loss += float(w)*F.cross_entropy(torch.unsqueeze(yh, dim=0), torch.tensor([self._class_to_index[y]], device=y_hat.device), weight=C)
                elif self._mlfl:
                    # Pick all labels normalized, with multi-label focal loss
                    #loss += float((1-yhs[self._class_to_index[y]])**2)*float(w)*F.cross_entropy(torch.unsqueeze(yh, dim=0), torch.tensor([self._class_to_index[y]], device=y_hat.device), weight=C)  # systemically penalizes non-multilabels                  
                    loss += torch.min(torch.tensor(1.0, device=y_hat.device), ((w-yhs[self._class_to_index[y]])/w)**2)*float(w)*F.cross_entropy(torch.unsqueeze(yh, dim=0), torch.tensor([self._class_to_index[y]], device=y_hat.device), weight=C)  
                elif self._mlbl:
                    # Pick all labels normalized with multi-label background loss
                    j = self._class_to_index['person'] if (y.startswith('person') or y.startswith('hand')) else self._class_to_index['vehicle']
                    #loss += float((1 - yhs[j])**2)*float((1-(yhs[self._class_to_index[y]]/w))**2)*float(w)*F.cross_entropy(torch.unsqueeze(yh, dim=0), torch.tensor([self._class_to_index[y]], device=y_hat.device), weight=C)                    
                    #loss += float((1 - yhs[j])**2)*float(w)*F.cross_entropy(torch.unsqueeze(yh, dim=0), torch.tensor([self._class_to_index[y]], device=y_hat.device), weight=C)   # will always predict background
                    loss += ((1-torch.sqrt(yhs[j]*yhs[self._class_to_index[y]]))**2)*float(w)*F.cross_entropy(torch.unsqueeze(yh, dim=0), torch.tensor([self._class_to_index[y]], device=y_hat.device), weight=C)  
                else:
                    # Pick all labels normalized (https://papers.nips.cc/paper/2019/file/da647c549dde572c2c5edc4f5bef039c-Paper.pdf
                    loss += float(w)*F.cross_entropy(torch.unsqueeze(yh, dim=0), torch.tensor([self._class_to_index[y]], device=y_hat.device), weight=C)

            n_valid += 1
        loss = loss / float(max(1, n_valid))  # batch reduction: mean

        if logging:
            self.log('train_loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return {'loss': loss}

    def validation_step(self, batch, batch_nb):
        loss = self.training_step(batch, batch_nb, logging=False, valstep=True)['loss']
        self.log('val_loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return {'val_loss': loss}

    def validation_end(self, outputs):
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        return {'avg_val_loss': avg_loss}
    # ---- </LIGHTNING>
    
    @classmethod
    def from_checkpoint(cls, checkpointpath):
        return cls().load_from_checkpoint(checkpointpath)  # lightning
            
    def _load_trained(self, ckptfile):
        self.net = pycollector.model.ResNets_3D_PyTorch.resnet.generate_model(50, n_classes=self.num_classes())
        t = torch.split(self.net.conv1.weight.data, dim=1, split_size_or_sections=1)
        self.net.conv1.weight.data = torch.cat( (*t, t[-1]), dim=1).contiguous()
        self.net.conv1.in_channels = 4  # inflate RGB -> RGBA
        self.load_state_dict(torch.load(ckptfile)['state_dict'])  # FIXME
        self.eval()
        return self
        
    def _load_pretrained(self):

        pthfile = vipy.util.tocache('r3d50_KMS_200ep.pth')
        if not os.path.exists(pthfile) or not vipy.downloader.verify_sha1(pthfile, '39ea626355308d8f75307cab047a8d75862c3261'):
            print('[pycollector.recognition]: Downloading pretrained weights ...')
            os.system('wget -c https://dl.dropboxusercontent.com/s/t3xge6lrfqpklr0/r3d50_kms_200ep.pth -O %s' % pthfile) 
        assert vipy.downloader.verify_sha1(pthfile, '39ea626355308d8f75307cab047a8d75862c3261'), "SHA1 check failed"

        net = pycollector.model.ResNets_3D_PyTorch.resnet.generate_model(50, n_classes=1139)
        pretrain = torch.load(pthfile, map_location='cpu')
        net.load_state_dict(pretrain['state_dict'])

        # Inflate RGB -> RGBA         
        t = torch.split(net.conv1.weight.data, dim=1, split_size_or_sections=1)
        net.conv1.weight.data = torch.cat( (*t, t[-1]), dim=1).contiguous()
        net.conv1.in_channels = 4

        self.net = net

        return self

    @staticmethod
    def _totensor(v, training, validation, input_size, num_frames, mean, std, noflip=None, show=False, doflip=False, zeropad=True):
        assert isinstance(v, vipy.video.Scene), "Invalid input"

        try:            
            v = v.download() if (not v.hasfilename() and v.hasurl()) else v  # fetch it if necessary, but do not do this during training!        
            if training or validation:
                (ai,aj) = (v.primary_activity().startframe(), v.primary_activity().endframe())  # activity (start,end)
                (ti,tj) = (v.actor().startframe(), v.actor().endframe())  # track (start,end) 
                startframe = np.random.randint(max(0, ti-(num_frames//2)), max(1, tj-(num_frames//2)))  # random startframe that contains track
                endframe = min((startframe+num_frames), aj)  # endframe truncated to be end of activity
                (startframe, endframe) = (startframe, endframe) if (startframe < endframe) else (max(0, aj-num_frames), aj)  # fallback
                assert endframe - startframe <= num_frames
                vc = v.clone().clip(startframe, endframe)    # may fail for some short clips
                vc = vc.trackcrop(dilate=1.2, maxsquare=True, zeropad=zeropad)  # may be None if clip contains no track
                vc = vc.resize(input_size, input_size)   # if zeropad=False, boxes near edges will not be square and will be anisotropically distorted, but will be faster
                vc = vc.fliplr() if (doflip or (np.random.rand() > 0.5)) and (noflip is None or vc.category() not in noflip) else vc
            else:
                vc = v.trackcrop(dilate=1.2, maxsquare=True, zeropad=zeropad)  # may be None if clip contains no track
                vc = vc if vc is not None else v.trackcrop(dilate=1.2, maxsquare=True, zeropad=True)  # fall back on zeropad if invalid
                vc = vc.resize(input_size, input_size)  # if zeropad=False, boxes near edges will not be square and will be anisotropically distorted, but will be faster
                vc = vc.fliplr() if doflip and (noflip is None or vc.category() not in noflip) else vc
                
            if show:
                vc.clone().resize(512,512).show(timestamp=True)
                vc.clone().binarymask().frame(0).rgb().show(figure='binary mask: frame 0')

            vc = vc.load(shape=(input_size, input_size, 3)).normalize(mean=mean, std=std, scale=1.0/255.0)  # [0,255] -> [0,1], triggers load() with known shape
            (t,lbl) = vc.torch(startframe=0, length=num_frames, boundary='cyclic', order='cdhw', withlabel=True)  # (c=3)x(d=num_frames)x(H=input_size)x(W=input_size), reuses vc._array -> t (requires t.clone())
            t = torch.cat((t.clone(), vc.channel(0).binarymask().float().bias(-0.5).torch(startframe=0, length=num_frames, boundary='cyclic', order='cdhw')), dim=0)  # (c=4) x (d=num_frames) x (H=input_size) x (W=input_size)

        except:
            if training or validation:
                #print('ERROR: %s' % (str(v)))
                t = torch.zeros(4, num_frames, input_size, input_size)  # skip me
                lbl = None
            else:
                print('WARNING: discarding tensor for video "%s"' % str(v))
                raise
                t = torch.zeros(4, num_frames, input_size, input_size)  # skip me (should never get here)
            
        if training or validation:
            return (t, json.dumps(lbl))  # json to use default collate_fn
        else:
            return t

    def totensor(self, v=None, training=False, validation=False, show=False, doflip=False, zeropad=True):
        """Return captured lambda function if v=None, else return tensor"""    
        assert v is None or isinstance(v, vipy.video.Scene), "Invalid input"
        f = (lambda v, num_frames=self._num_frames, input_size=self._input_size, mean=self._mean, std=self._std, training=training, validation=validation, show=show, zeropad=zeropad:
             PIP_250k._totensor(v, training, validation, input_size, num_frames, mean, std, noflip=['car_turns_left', 'car_turns_right'], show=show, doflip=doflip, zeropad=zeropad))
        return f(v) if v is not None else f
    

class ActivityTracker(PIP_250k):
    def __init__(self, stride=1, activities=None, gpus=None, batchsize=None, mlbl=False, mlfl=False, modelfile=None):
        #modelfile = '/disk1/diva/visym/epoch=18-step=10620.ckpt'
        #modelfile = '/disk1/diva/visym/epoch=19-step=11179.ckpt'
        #modelfile = '/disk1/diva/visym/epoch=30-step=17328.ckpt'
        #modelfile = '/disk1/diva/visym/mlfl_epoch=9-step=11169.ckpt'
        #modelfile = '/disk1/diva/visym/epoch=12-step=14520.ckpt'   # mlfl
        #modelfile = '/disk1/diva/visym/mlfl_epoch=15-step=17871.ckpt' if modelfile is None else modelfile 
        #modelfile = '/disk1/diva/visym/epoch_23-step_26807_3.ckpt' if modelfile is None else modelfile
        #modelfile = '/disk1/diva/visym/mlfl_0060_epoch_12-step_14520.ckpt' if modelfile is None else modelfile  # 0065
        assert modelfile is not None

        super().__init__(pretrained=False, modelfile=modelfile, mlbl=mlbl, mlfl=mlfl)
        self._stride = stride
        self._allowable_activities = {k:v for (k,v) in [(a,a) if not isinstance(a, tuple) else a for a in activities]} if activities is not None else {k:k for k in self.classlist()}
        self._batchsize_per_gpu = batchsize
        self._gpus = gpus

        if gpus is not None:
            assert torch.cuda.is_available()
            assert batchsize is not None
            self._devices = ['cuda:%d' % k for k in gpus]
            self._gpus = [copy.deepcopy(self.net).to(d, non_blocking=False) for d in self._devices]  
            for m in self._gpus:
                m.eval()

    def temporal_stride(self, s=None):
        if s is not None:
            self._stride = s
            return self
        else:
            return self._stride

    def forward(self, x):
        """Overload forward for multi-gpu batch.  Don't use torch DataParallel!"""
        if self._gpus is None:
            return super().forward(x)  # cpu
        else:
            x_forward = None
            for b in x.split(self._batchsize_per_gpu*len(self._gpus)):
                todevice = [t.pin_memory().to(d, non_blocking=True) for (t,d) in zip(b.split(self._batchsize_per_gpu), self._devices)]  # async?
                ondevice = [m(t) for (m,t) in zip(self._gpus, todevice)]   # async?
                fromdevice = torch.cat([t.detach().cpu() for t in ondevice], dim=0)
                x_forward = fromdevice if x_forward is None else torch.cat((x_forward, fromdevice), dim=0)
                del ondevice, todevice, fromdevice, b  # force garbage collection of GPU memory
            del x  # force garbage collection
            return x_forward

    def __call__(self, vi, topk=1, activityiou=0, mirror=False, minprob=0, trackconf=0.1, maxdets=None):
        (n,m) = (self.temporal_support(), self.temporal_stride())
        aa = self._allowable_activities  # dictionary mapping of allowable classified activities to output names        
        f_nomirror = self.totensor(training=False, validation=False, show=False, doflip=False, zeropad=True)  # test video -> tensor
        f_mirror = self.totensor(training=False, validation=False, show=False, doflip=True, zeropad=True)  # test video -> tensor mirrored
        f_totensor = lambda v: (torch.unsqueeze(f_nomirror(v.clone(sharedarray=True)), dim=0) if (not mirror or v.actor().category() != 'person') else torch.stack((f_nomirror(v.clone(sharedarray=True)), f_mirror(v)), dim=0))
        def f_reduce(T,V):
            j = sum([v.actor().category() == 'person' for v in V])  # person mirrored, vehicle not mirrored
            (tm, t) = torch.split(T, (2*j, len(T)-2*j), dim=0)  # assumes sorted order, person first, only person/vehicle
            return torch.cat((torch.mean(tm.view(-1, 2, tm.shape[1]), dim=1), t), dim=0) if j>0 else T  # mean over mirror augmentation
            
        try:
            vp = next(vi)  # peek in generator to create clip
            vi = itertools.chain([vp], vi)  # unpeek
            for (k, (vc,v)) in enumerate(zip(vp.stream().clip(n, m, continuous=True), vi)):
                videotracks = [] if vc is None else [vt for vt in vc.tracksplit() if len(vt.actor())>0 and vt.actor().category() == 'person' or (vt.actor().category() == 'vehicle' and v.track(vt.actorid()).ismoving(k-3*n, k))]  # vehicle moved in last 3 clips (~10s)?
                videotracks = sorted(videotracks, key=lambda v: v.actor().confidence(last=1))[-maxdets:] if maxdets is not None else videotracks  # sort by track confidence, and select only the most confident for detection
                videotracks = sorted(videotracks, key=lambda v: v.actor().category())  # for grouping mirrored encoding: person<vehicle
                if len(videotracks)>0 and (k > n):
                    logits = self.forward(torch.cat([f_totensor(vt) for vt in videotracks], dim=0))  # augmented logits in track index order
                    logits = f_reduce(logits, videotracks) if mirror else logits  # reduced logits in track index order
                    dets = [vipy.activity.Activity(category=aa[category], shortlabel=self._class_to_shortlabel[category], startframe=k-n, endframe=k, confidence=conf, framerate=v.framerate(), actorid=videotracks[j].actorid(), attributes={'pip':category}) 
                            for (j, categoryconfprob) in enumerate(super().topk_probability(logits, topk))  # top-k activities
                            for (category, conf, prob) in categoryconfprob   # top-k categories, confidence, probability for tensor
                            if ((category in aa) and   # requested activities only
                                (videotracks[j].actor().category() in self._verb_to_noun[category]) and   # noun matching with category renaming dictionary
                                prob>minprob)]   # minimum probability for new activity detection
                    v.assign(k, dets, activityiou=activityiou)   # assign new activity detections by merging overlapping activities with weighted average of probability
                    del logits, dets, videotracks  # torch garabage collection
                yield v

        except Exception as e:                
            raise

        finally:
            # Bad tracks:  Remove low confidence or too short non-moving tracks
            v.trackfilter(lambda t: len(t)>=2*v.framerate() and (t.confidence() >= trackconf or t.startbox().iou(t.endbox()) == 0)).activityfilter(lambda a: a.actorid() in v.tracks())

            # Activity probability:  Track probability * activity probability
            v.activitymap(lambda a: a.confidence(float(1.0 / (1.0 + np.exp(-(a.confidence() + 1.0))))))   # activity confidence -> probability
            v.activitymap(lambda a: a.confidence(v.track(a.actorid()).confidence(samples=8)*a.confidence()))  # "independent" probabilities

            # Poor classes:  Significantly reduce confidence of complex classes (yuck)
            v.activitymap(lambda a: a.confidence(0.05*a.confidence()) if (a.category() in ['person_steals_object', 'person_abandons_package']) else a)

            # Vehicle track:  High confidence vehicle turns must be a minimum angle
            v.activitymap(lambda a: a.confidence(0.2*a.confidence()) if ((a.category() in ['vehicle_turns_left', 'vehicle_turns_right']) and (abs(v.track(a.actorid()).bearing_change(a.startframe(), a.endframe(), dt=2*v.framerate())) < (np.pi/8))) else a)

            # Vehicle track:  U-turn can only be distinguished from left/right turn at the end of a track by looking at the turn angle
            v.activitymap(lambda a: a.category('vehicle_makes_u_turn').shortlabel('u turn') if ((a.category() in ['vehicle_turns_left', 'vehicle_turns_right']) and (abs(v.track(a.actorid()).bearing_change(a.startframe(), a.endframe(), dt=2*v.framerate())) > (np.pi-(np.pi/8)))) else a)

            # Vehicle track: Starts and stops must be at most 5 seconds (yuck)
            v.activitymap(lambda a: a.truncate(a.startframe(), a.startframe()+v.framerate()*5) if a.category() in ['vehicle_starts', 'vehicle_reverses'] else a)
            v.activitymap(lambda a: a.truncate(a.endframe()-5*v.framerate(), a.endframe()) if a.category() == 'vehicle_stops' else a)
            v.activitymap(lambda a: a.truncate(a.middleframe()-2.5*v.framerate(), a.middleframe()+2.5*v.framerate()) if a.category() in ['vehicle_turns_left', 'vehicle_turns_right', 'vehicle_makes_u_turn'] else a)   
                          
            # Person/Bicycle track: riding must be accompanied by an associated moving bicycle track
            v.activitymap(lambda a: a.confidence(0.01*a.confidence()) if ((a.category() == 'person_rides_bicycle') and not any([t.category() == 'bicycle' and
                                                                                                                                t.segment_maxiou(v.track(a.actorid()), a.startframe(), a.endframe()) > 0 and
                                                                                                                                t.ismoving(a.startframe(), a.endframe())
                                                                                                                                for t in v.tracklist()])) else a)

            # Person/Vehicle track: person/vehicle interaction must be accompanied by an associated stopped vehicle track
            v.activitymap(lambda a: a.confidence(0.01*a.confidence()) if ((a.category().startswith('person') and ('vehicle' in a.category() or 'trunk' in a.category())) and not any([t.category() == 'vehicle' and
                                                                                                                                                                                      t.segment_maxiou(v.track(a.actorid()), a.startframe(), a.endframe()) > 0 and
                                                                                                                                                                                      not t.ismoving(a.startframe(), a.endframe())
                                                                                                                                                                                      for t in v.tracklist()])) else a)
            # Vehicle/Person track: vehicle/person interaction must be accompanied by an associated person track
            v.activitymap(lambda a: a.confidence(0.01*a.confidence()) if ((a.category().startswith('vehicle') and ('person' in a.category())) and not any([t.category() == 'person' and t.segment_maxiou(v.track(a.actorid()), a.startframe(), a.endframe()) > 0 for t in v.tracklist()])) else a)

            # Vehicle/Person track: vehicle dropoff/pickup must be accompanied by an associated person track start/end
            v.activitymap(lambda a: a.confidence(0.01*a.confidence()) if (a.category() == 'vehicle_drops_off_person' and not any([t.category() == 'person' and t.segment_maxiou(v.track(a.actorid()), t.startframe(), t.startframe()+1) > 0 for t in v.tracklist()])) else a)
            v.activitymap(lambda a: a.confidence(0.01*a.confidence()) if (a.category() == 'vehicle_picks_up_person' and not any([t.category() == 'person' and t.segment_maxiou(v.track(a.actorid()), t.endframe()-1, t.endframe()) > 0 for t in v.tracklist()])) else a)
            
            # Person track: enter/exit scene cannot be at the image boundary 
            v.activitymap(lambda a: a.confidence(0.01*a.confidence()) if (a.category() == 'person_enters_scene_through_structure' and v.track(a.actorid())[max(a.startframe(), v.track(a.actorid()).startframe())].cover(v.framebox().dilate(0.9)) < 1) else a)
            v.activitymap(lambda a: a.confidence(0.01*a.confidence()) if (a.category() == 'person_exits_scene_through_structure' and v.track(a.actorid())[min(a.endframe(), v.track(a.actorid()).endframe())].cover(v.framebox().dilate(0.9)) < 1) else a)
                        
            # Activity union:  Temporal gaps less than support should be merged into one activity detection for a single track
            merged = set([])
            for a in sorted(v.activitylist(), key=lambda a: a.startframe()):
                for o in sorted(v.activitylist(), key=lambda a: a.startframe()):  # other
                    if (o.startframe() >= a.startframe()) and (a.id() != o.id()) and (o.actorid() == a.actorid()) and (o.category() == a.category()) and (o.id() not in merged) and (a.id() not in merged) and (a.temporal_distance(o) <= self.temporal_support()): 
                        a.union(o)  # in-place update
                        merged.add(o.id())
            v.activityfilter(lambda a: a.id() not in merged)

            # Activity union:  "Brief" breaks of these activities should be merged into one activity detection for a single track
            tomerge = set(['person_reads_document', 'person_interacts_with_laptop', 'person_talks_to_person', 'person_purchases', 'person_steals_object', 'person_talks_on_phone', 'person_texts_on_phone', 'person_rides_bicycle', 'person_carries_heavy_object'])
            merged = set([])
            for a in sorted(v.activitylist(), key=lambda a: a.startframe()):
                if a.category() in tomerge:
                    for o in sorted(v.activitylist(), key=lambda a: a.startframe()):  # other
                        if (o.startframe() >= a.startframe()) and (o.id() != a.id()) and (o.actorid() == a.actorid()) and (o.category() == a.category()) and (o.id() not in merged) and (a.id() not in merged) and (a.temporal_distance(o) < 10*v.framerate()):  # "brief" == "<10s"
                            a.union(o)  # in-place update
                            merged.add(o.id())
            v.activityfilter(lambda a: a.id() not in merged)            

            # Activity group suppression:  Group activities may have at most one activity detection of this type per group in a spatial region surrounding the actor
            tosuppress = set(['hand_interacts_with_person', 'person_embraces_person', 'person_transfers_object', 'person_steals_object', 'person_purchases', 'person_talks_to_person'])
            suppressed = set([])
            for a in sorted(v.activitylist(), key=lambda a: a.confidence(), reverse=True):  # decreasing confidence
                if a.category() in tosuppress:
                    for o in v.activitylist():  # other activities
                        if (o.actorid() != a.actorid() and  # different tracks
                            o.category() == a.category() and  # same category
                            o.confidence() <= a.confidence() and   # lower confidence
                            o.id() not in suppressed and  # not already suppressed
                            o.during_interval(a.startframe(), a.endframe()) and # overlaps temporally by at least one frame
                            (v.track(a.actorid()).boundingbox(a.startframe(), a.endframe()) is not None and v.track(o.actorid()).boundingbox(a.startframe(), a.endframe()) is not None) and   # has valid tracks
                            (v.track(a.actorid()).boundingbox(a.startframe(), a.endframe()).dilate(1.2).maxsquare().iou(v.track(o.actorid()).boundingbox(a.startframe(), a.endframe()).dilate(1.2).maxsquare()) > 0)):  # overlaps spatially "close by"
                            suppressed.add(o.id())  # greedy non-maximum suppression of lower confidence activity detection
            v.activityfilter(lambda a: a.id() not in suppressed)
            v.setattribute('_completed', str(datetime.now()))

