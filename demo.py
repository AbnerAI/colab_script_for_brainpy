import brainpy as bp
import brainpy.math as bm

bm.set_platform('cpu')
bp.__version__
E = bp.neurons.LIF(3200, V_rest=-60., V_th=-50., V_reset=-60.,
                   tau=20., tau_ref=5., method='exp_auto',
                   V_initializer=bp.init.Normal(-60., 2.))

I = bp.neurons.LIF(800, V_rest=-60., V_th=-50., V_reset=-60.,
                   tau=20., tau_ref=5., method='exp_auto',
                   V_initializer=bp.init.Normal(-60., 2.))
E2E = bp.synapses.Exponential(E, E, bp.conn.FixedProb(prob=0.02), g_max=0.6,
                              tau=5., output=bp.synouts.COBA(E=0.),
                              method='exp_auto')

E2I = bp.synapses.Exponential(E, I, bp.conn.FixedProb(prob=0.02), g_max=0.6,
                              tau=5., output=bp.synouts.COBA(E=0.),
                              method='exp_auto')

I2E = bp.synapses.Exponential(I, E, bp.conn.FixedProb(prob=0.02), g_max=6.7,
                              tau=10., output=bp.synouts.COBA(E=-80.),
                              method='exp_auto')

I2I = bp.synapses.Exponential(I, I, bp.conn.FixedProb(prob=0.02), g_max=6.7,
                              tau=10., output=bp.synouts.COBA(E=-80.),
                              method='exp_auto')
net = bp.Network(E2E, E2I, I2E, I2I, E=E, I=I)
runner = bp.DSRunner(net,
                     monitors=['E.spike', 'I.spike'],
                     inputs=[('E.input', 20.), ('I.input', 20.)],
                     dt=0.1)
runner.run(100)
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4.5))

plt.subplot(121)
bp.visualize.raster_plot(runner.mon.ts, runner.mon['E.spike'], show=False)
plt.subplot(122)
bp.visualize.raster_plot(runner.mon.ts, runner.mon['I.spike'], show=False)

plt.savefig("demo.png")