# ***************************************************************
# Copyright (c) 2021 Jittor. All Rights Reserved. 
# Maintainers:
#     Guowei Yang <471184555@qq.com>
#     Guoye Yang <498731903@qq.com>
#     Wenyang Zhou <576825820@qq.com>
#     Meng-Hao Guo <guomenghao1997@gmail.com>
#     Dun Liang <randonlang@gmail.com>.
#
# 
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
import jittor as jt
import numpy as np

class Optimizer(object):
    """ Basic class of Optimizer.

    Example::

        optimizer = nn.SGD(model.parameters(), lr)
        optimizer.step(loss)
    """
    def __init__(self, params, lr, param_sync_iter=10000):
        self.param_groups = []
        self.lr = lr
        self.param_sync_iter = param_sync_iter

        assert len(params) > 0, "Length of parameters should not be zero"
        if not isinstance(params[0], dict):
            params = [{'params': params}]
        for pg in params:
            assert isinstance(pg, dict)
            self.param_groups.append(pg)
        self.n_step = 0

    def add_param_group(self, group):
        self.param_groups.append(group)
    
    @property
    def defaults(self):
        exclude = set(("defaults", "param_groups", "n_step", "pre_step", "step"))
        return { k:v for k, v in self.__dict__.items()
            if k[0] != '_' and k not in exclude and not callable(v) }

    def pre_step(self, loss):
        """ something should be done before step, such as calc gradients, mpi sync, and so on.

        Example::

            class MyOptimizer(Optimizer):
                def step(self, loss):
                    self.post_step(loss)
                    ...
        """
        # clean prev grads
        params = []
        params_has_grad = []
        for pg in self.param_groups:
            pg["grads"] = [None] * len(pg['params'])
            for p in pg['params']:
                params.append(p)
                if not p.is_stop_grad():
                    params_has_grad.append(p)

        # get gradient
        grads = jt.grad(loss, params_has_grad)

        # sync grads and model if in mpi
        if jt.in_mpi:
            for g in grads:
                g.assign(g.mpi_all_reduce("mean"))
            if self.n_step % self.param_sync_iter == 0:
                for p in params:
                    p.assign(p.mpi_broadcast())
        self.n_step += 1

        # set up grads in param_groups
        pid = 0
        for pg in self.param_groups:
            pg_grads = pg["grads"]
            for i, p in enumerate(pg['params']):
                if not p.is_stop_grad():
                    # stop grad of grad
                    pg_grads[i] = grads[pid].stop_grad()
                    pid += 1
        
    def backward(self, loss):
        self.pre_step(loss)

    def step(self, loss=None):
        if loss is not None:
            self.pre_step(loss)
        for pg in self.param_groups:
            lr = pg.get("lr", self.lr)
            for p, g in zip(pg["params"], pg["grads"]):
                if p.is_stop_grad(): continue
                p.update(p - g * lr)


class SGD(Optimizer):
    """ SGD Optimizer.

    Example::

        optimizer = nn.SGD(model.parameters(), lr, momentum=0.9)
        optimizer.step(loss)
    """
    def __init__(self, params, lr, momentum=0, weight_decay=0, dampening=0, nesterov=False):
        super().__init__(params, lr)
        self.momentum = momentum
        self.weight_decay = weight_decay
        self.dampening = dampening
        self.nesterov = nesterov

        # initialize required arguments
        for pg in self.param_groups:
            values = pg["values"] = []
            for p in pg["params"]:
                values.append(jt.zeros(p.shape, p.dtype).stop_grad())

    def add_param_group(self, group):
        values = group["values"] = []
        for p in group["params"]:
            values.append(jt.zeros(p.shape, p.dtype).stop_grad())
        self.param_groups.append(group)

    def step(self, loss=None):
        if loss is not None:
            self.pre_step(loss)
        for pg in self.param_groups:
            # get arguments from each param_groups
            lr = pg.get("lr", self.lr)
            momentum = pg.get("momentum", self.momentum)
            weight_decay = pg.get("weight_decay", self.weight_decay)
            dampening = pg.get("dampening", self.dampening)
            nesterov = pg.get("nesterov", self.nesterov)

            # optimize main body
            for p, g, v in zip(pg["params"], pg["grads"], pg["values"]):
                if p.is_stop_grad(): continue
                dp = p * weight_decay + g
                v.update(momentum * v + dp * (1 - dampening))
                if nesterov:
                    p.update(p - (dp + momentum * v) * lr)
                else:
                    p.update(p - v * lr)

class RMSprop(Optimizer):
    """ RMSprop Optimizer.
    Args:
        params(list): parameters of model.
        lr(float): learning rate.
        eps(float): term added to the denominator to avoid division by zero, default 1e-8.
        alpha(float): smoothing constant, default 0.99.

    Example:
        optimizer = nn.RMSprop(model.parameters(), lr)
        optimizer.step(loss)
    """
    def __init__(self, params, lr=1e-2, eps=1e-8, alpha=0.99):
        super().__init__(params, lr)
        self.eps = eps
        self.alpha = alpha
        
        # initialize required arguments for each param_groups
        for pg in self.param_groups:
            values = pg["values"] = []
            for p in pg["params"]:
                values.append(jt.zeros(p.shape, p.dtype).stop_grad())

    def add_param_group(self, group):
        values = group["values"] = []
        for p in group["params"]:
            values.append(jt.zeros(p.shape, p.dtype).stop_grad())
        self.param_groups.append(group)

    def step(self, loss=None):
        if loss is not None:
            self.pre_step(loss)
        for pg in self.param_groups:
            # get arguments from each param_groups
            lr = pg.get("lr", self.lr)
            eps = pg.get("eps", self.eps)
            alpha = pg.get("alpha", self.alpha)
            for p, g, v in zip(pg["params"], pg["grads"], pg["values"]):
                if p.is_stop_grad(): continue
                v.update(alpha * v + (1-alpha) * g * g)
                p.update(p - lr * g / (jt.sqrt(v) + eps))

class Adam(Optimizer):
    """ Adam Optimizer.
    
    Example::

        optimizer = nn.Adam(model.parameters(), lr, eps=1e-8, betas=(0.9, 0.999))
        optimizer.step(loss)
    """
    def __init__(self, params, lr, eps=1e-8, betas=(0.9, 0.999), weight_decay=0):
        super().__init__(params, lr)
        self.eps = eps
        self.betas = betas
        # self.weight_decay = weight_decay
        assert weight_decay==0, "weight_decay is not supported yet"
        
        # initialize required arguments for each param_groups
        for pg in self.param_groups:
            values = pg["values"] = []
            m = pg["m"] = []
            for p in pg["params"]:
                values.append(jt.zeros(p.shape, p.dtype).stop_grad())
                m.append(jt.zeros(p.shape, p.dtype).stop_grad())

    def add_param_group(self, group):
        values = group["values"] = []
        m = group["m"] = []
        for p in group["params"]:
            values.append(jt.zeros(p.shape, p.dtype).stop_grad())
            m.append(jt.zeros(p.shape, p.dtype).stop_grad())
        self.param_groups.append(group)

    def step(self, loss=None):
        if loss is not None:
            self.pre_step(loss)
        n = float(self.n_step)
        for pg in self.param_groups:
            # get arguments from each param_groups
            lr = pg.get("lr", self.lr)
            eps = pg.get("eps", self.eps)
            b0, b1 = pg.get("betas", self.betas)
            for p, g, v, m in zip(pg["params"], pg["grads"], pg["values"], pg["m"]):
                if p.is_stop_grad(): continue
                m.update(b0 * m + (1-b0) * g)
                v.update(b1 * v + (1-b1) * g * g)
                step_size = lr * jt.sqrt(1-b1**n) / (1-b0 ** n)
                p.update(p - m * step_size / (jt.sqrt(v) + eps))


class LRScheduler:
    def __init__(self,optimizer, last_epoch=-1):
        assert isinstance(optimizer,Optimizer)
        self.optimizer = optimizer
        
        if last_epoch==-1:
            for gp in optimizer.param_groups:
                gp.setdefault('initial_lr',gp.get('lr',optimizer.lr))
        else:
            for gp in optimizer.param_groups:
                assert 'initial_lr' in gp 
        
        self.base_lrs = list(map(lambda group: group['initial_lr'], optimizer.param_groups))
        self.last_epoch = last_epoch
        self.optimizer._step_count = 0
        self._step_count = 0
        self.step()

    def get_lr(self):
        raise NotImplementedError 
    
    def get_last_lr(self):
        return self._last_lr

    def step(self,epoch=None):
        self._step_count += 1

        if epoch is None:
            self.last_epoch += 1
            values = self.get_lr()
        else:
            self.last_epoch = epoch
            values = self.get_lr()

        for i, data in enumerate(zip(self.optimizer.param_groups, values)):
            param_group, lr = data
            param_group['lr'] = lr

        self._last_lr = [group['lr'] for group in self.optimizer.param_groups]


class LambdaLR(LRScheduler):

    def __init__(self, optimizer, lr_lambda, last_epoch=-1):
        if not isinstance(lr_lambda, list) and not isinstance(lr_lambda, tuple):
            self.lr_lambdas = [lr_lambda] * len(optimizer.param_groups)
        else:
            if len(lr_lambda) != len(optimizer.param_groups):
                raise ValueError("Expected {} lr_lambdas, but got {}".format(len(optimizer.param_groups), len(lr_lambda)))

            self.lr_lambdas = list(lr_lambda)
            
        super(LambdaLR, self).__init__(optimizer, last_epoch)
        
        

    def get_lr(self):
        return [base_lr * lmbda(self.last_epoch)
                for lmbda, base_lr in zip(self.lr_lambdas, self.base_lrs)]