import panel as pn
import holoviews as hv

from holoviews import opts

hv.extension('bokeh')


def MakePanel(holo_df, 
              kdims=['date', 'Utility', 'Interval'], 
              vdims=['Consumption', 'Cost']):
    intervals = list(holo_df[kdims[2]].unique())
    intervals = pn.widgets.RadioButtonGroup(options=intervals, name=kdims[2])
    holo_ds = hv.Dataset(holo_df, kdims, vdims)
    plot = holo_ds.to(hv.Curve, kdims[0], vdims[0])
    plot = plot.opts(opts.Curve(framewise=True, tools=['hover'],
                                aspect=2/1, responsive=True))
    pan = plot.layout(kdims[1]).opts(tabs=True, framewise=True)
    pan = pn.panel(pan, widgets={kdims[2]: intervals})
    return pn.Column(f"# {kdims[1]} {vdims[0]} per {kdims[2]}",
                     pan[0], 
                     pn.Row(pn.layout.HSpacer(), pan[1][0], pn.layout.HSpacer()),
                     width_policy='max')


