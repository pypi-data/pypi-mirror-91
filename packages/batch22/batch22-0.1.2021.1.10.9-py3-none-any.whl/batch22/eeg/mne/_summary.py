#!/usr/bin/env ipython
# -*- coding: utf-8 -*


from ipywidgets import interactive,Dropdown,SelectMultiple
from collections import OrderedDict
import pandas as pd
import pingouin as pg
import seaborn as sns
import matplotlib as mpt
import matplotlib.pyplot as plt


class SummaryMNE():
    def __init__(self,df0,within=["cond0","clust0"],height=6,aspect=1,sample=0):
        self.df0            = df0.copy()
        self.df1            = self.df0.copy()[["epochs0","tool0","mode0","type0","cond0","chan0","later0","front0","clust0","tmin0"]].drop_duplicates()
        self.height         = height
        self.aspect         = aspect
        self.within         = within
        self.epochs0_widget = Dropdown(options = df0.epochs0.unique().tolist())
        self.tool0_widget   = Dropdown()
        self.mode0_widget   = Dropdown()
        self.type0_widget   = Dropdown()
        self.tmin0_widget   = Dropdown()
        self.cond0_widget   = SelectMultiple(options=["word"],value=["word"],rows=9,description="cond0")
        self.epochs0_widget .observe(self.epochs0_updated)
        self.tool0_widget   .observe(self.tool0_updated)
        self.mode0_widget   .observe(self.mode0_updated)
        self.type0_widget   .observe(self.type0_updated)
        self.tmin0_widget   .observe(self.tmin0_updated)
        self.interact       = interactive(
            self.g_function,
            epochs0 = self.epochs0_widget,
            tool0   = self.tool0_widget,
            mode0   = self.mode0_widget,
            type0   = self.type0_widget,
            tmin0   = self.tmin0_widget,
            cond0   = self.cond0_widget,
        )

    def epochs0_updated(self,*args):
        self.tool0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value)
        ].tool0.unique().tolist()
        self.tool0_updated(*args)

    def tool0_updated(self,*args):
        self.mode0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value)
        ].mode0.unique().tolist()
        self.mode0_updated(*args)

    def mode0_updated(self,*args):
        self.type0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value) &
            (self.df1.mode0   == self.mode0_widget  .value)
        ].type0.unique().tolist()
        self.type0_updated(*args)

    def type0_updated(self,*args):
        self.tmin0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value) &
            (self.df1.mode0   == self.mode0_widget  .value) &
            (self.df1.type0   == self.type0_widget  .value)
        ].tmin0.unique().tolist()
        self.tmin0_updated(*args)

    def tmin0_updated(self,*args):
        self.cond0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value) &
            (self.df1.mode0   == self.mode0_widget  .value) &
            (self.df1.type0   == self.type0_widget  .value) &
            (self.df1.tmin0   == self.tmin0_widget  .value)
        ].cond0.unique().tolist()

    def g_function(self,epochs0,tool0,mode0,type0,tmin0,cond0):
        self.df2 = self.df0[
            (self.df0.epochs0 == epochs0) &
            (self.df0.tool0   == tool0  ) &
            (self.df0.mode0   == mode0  ) &
            (self.df0.type0   == type0  ) &
            (self.df0.tmin0   == tmin0  )
        ].copy()
        if not cond0:
            cond0 = self.df1.cond0.unique().tolist()

        self.df3 = self.df2[self.df2.cond0.isin(cond0)].copy()
        ARGS = OrderedDict()
        ARGS["data"]       = self.df3.copy()
        ARGS["dv"]         = "valX"
        ARGS["within"]     = self.within
        ARGS["subject"]    = "subj0"
        ARGS["correction"] = "auto"
        ARGS["detailed"]   = False
        ARGS["effsize"]    = "np2" # "np2" "n2" "ng2"
        AOV  = pg.rm_anova(**ARGS)
        display(AOV.round(3))
        print("epochs0: {}".format(epochs0))
        print("tool0: {}"  .format(tool0  ))
        print("mode0: {}"  .format(mode0  ))
        print("type0: {}"  .format(type0  ))
        print("tmin0: {}"  .format(tmin0  ))
        print("cond0: {}"  .format(cond0  ))
        print("N: {}"      .format(self.df3.shape[0]))
        print("within: {}" .format(self.within))
        sns.catplot(
            x       = ARGS["within"][1],
            y       = ARGS["dv"],
            hue     = ARGS["within"][0],
            data    = ARGS["data"],
            kind    = "bar",
            palette = "Set2",
            height  = self.height,
            aspect  = self.aspect,
        )
        plt.show()
        display(ARGS["data"].groupby("cond0").agg(["count","mean","std"])["valX"])
        display(ARGS["data"].groupby(ARGS["within"]).agg(["count","mean","std"])["valX"])
        if self.sample:
            display(ARGS["data"].sample(n=12).sort_index())
