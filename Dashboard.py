import panel as pn
import holoviews as hv

from holoviews import opts

hv.extension('bokeh')


def MakePanel(holo_df, 
              kdims=['date', 'Utility', 'Interval'], 
              vdims=['Consumption', 'Cost']):
    
    holo_ds = hv.Dataset(holo_df, kdims, vdims)
    intervals = MakeIntervalWidget(holo_df, kdims)
    pan = GetConsumptionPanel(holo_ds, kdims, vdims, intervals)
    ints = MakeIntervalWidget(holo_df, kdims)
    c_cost = GetCostPanel(holo_ds, kdims, vdims, ints)
    return pn.Column(f"## {kdims[1]} {vdims[0]} per {kdims[2]}",
                     pn.Row(pan[0], margin=(0, 10, 10, 10)),
                     pn.layout.Spacer(),
                     pn.Row(pn.layout.HSpacer(), pan[1][0], pn.layout.HSpacer()),
                     pn.layout.Spacer(),
                     f"## {kdims[1]} {vdims[1]} per {kdims[2]}",
                     pn.Row(c_cost[0], margin=(0, 10, 10, 10)),
                     pn.layout.Spacer(),
                     pn.Row(pn.layout.HSpacer(), c_cost[1][0], pn.layout.HSpacer()),
                     margin=40)


def GetConsumptionPanel(holo_ds, kdims, vdims, intervals):
    plot = holo_ds.to(hv.Curve, kdims[0], vdims[0])
    plot = plot.opts(opts.Curve(framewise=True, tools=['hover'],
                                aspect=2/1, responsive=True,
                                max_width=1500))
    pan = plot.layout(kdims[1]).opts(tabs=True, shared_axes=False)
    pan = pn.panel(pan, widgets={kdims[2]: intervals}, margin=5)
    pan[1][0][0].margin = 0
    return pan


def GetCostPanel(holo_ds, kdims, vdims, intervals):
    c_cost = holo_ds.to(hv.Curve, kdims[0], vdims[1])
    c_cost = c_cost.opts(opts.Curve(framewise=True, tools=['hover'],
                                    aspect=2/1.5, responsive=True,
                                    max_width=1500))
    c_cost = c_cost.overlay(kdims[1])
    c_cost = c_cost.opts(legend_position='top')
    c_cost = pn.panel(c_cost, widgets={kdims[2]: intervals}, margin=5)
    c_cost[1][0][0].margin = 0
    return c_cost


def MakeIntervalWidget(holo_df, kdims):
    intervals = list(holo_df[kdims[2]].unique())
    intervals = pn.widgets.RadioButtonGroup(options=intervals, 
                                            name=kdims[2],
                                            margin=(10,10,10,10))
    return intervals