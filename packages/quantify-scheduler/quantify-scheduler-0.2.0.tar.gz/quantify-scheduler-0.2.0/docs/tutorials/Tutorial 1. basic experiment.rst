.. _sec-tutorial1:

Tutorial 1. Basic experiments
================================

.. jupyter-kernel::
  :id: Tutorial 1. Basic experiment

.. tip::
    Following this Tutorial requires familiarity with the **core concepts** of Quantify-scheduler, we **highly recommended** to consult the (short) :ref:`User guide` before proceeding.


The benefit of allowing the user to mix the high-level gate description of a circuit with the lower-level pulse description can be understood through an example.
Below we first give an example of basic usage using `Bell violations`.
We next show the `Chevron` experiment in which the user is required to mix gate-type and pulse-type information when defining the :class:`~quantify.scheduler.Schedule`.

Basics: The Bell experiment
-----------------------------

As the first example, we want to perform the `Bell experiment <https://en.wikipedia.org/wiki/Bell%27s_theorem>`_ .
The goal of the Bell experiment is to create a Bell state :math:`|\Phi ^+\rangle=\frac{1}{2}(|00\rangle+|11\rangle)` followed by a measurement.
By rotating the measurement basis, or equivalently one of the qubits, it is possible to observe violations of the CSHS inequality.
If everything is done properly, one should observe the following oscillation:

.. jupyter-execute::
  :hide-code:

  import plotly.graph_objects as go
  import numpy as np

  x = np.linspace(0, 360, 361)
  y = np.cos(np.deg2rad(x-180))
  yc = np.minimum(x/90-1, -x/90+3)


  fig = go.Figure()
  fig.add_trace(go.Scatter(x=x,y=y, name='Quantum'))
  fig.add_trace(go.Scatter(x=x,y=yc, name='Classical'))

  fig.update_layout(title='Bell experiment',
                     xaxis_title='Angle between detectors (deg)',
                     yaxis_title='Correlation')
  fig.show()


Bell circuit
~~~~~~~~~~~~~~~~
We create this experiment using :ref:`gates acting on qubits<Gate-level description>` .


We start by initializing an empty :class:`~quantify.scheduler.Schedule`

.. jupyter-execute::

  from quantify.scheduler import Schedule
  sched = Schedule('Bell experiment')
  sched

Under the hood, the :class:`~quantify.scheduler.Schedule` is based on a dictionary that can be serialized

.. jupyter-execute::

  sched.data

We also need to define the qubits.

.. jupyter-execute::

  q0, q1 = ('q0', 'q1') # we use strings because qubit resources have not been implemented yet.

Creating the circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will now add some operations to the schedule.
Because this experiment is most conveniently described on the gate level, we use operations defined in the :mod:`quantify.scheduler.gate_library` .

.. jupyter-execute::

    from quantify.scheduler.gate_library import Reset, Measure, CZ, Rxy, X90
    import numpy as np

    # we use a regular for loop as we have to unroll the changing theta variable here
    for theta in np.linspace(0, 360, 21):
        sched.add(Reset(q0, q1))
        sched.add(X90(q0))
        sched.add(X90(q1), ref_pt='start') # this ensures pulses are aligned
        sched.add(CZ(q0, q1))
        sched.add(Rxy(theta=theta, phi=0, qubit=q0))
        sched.add(Measure(q0, q1), label='M {:.2f} deg'.format(theta))


Visualizing the circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

And we can use this to create a default visualization:

.. jupyter-execute::

  %matplotlib inline

  from quantify.scheduler.visualization.circuit_diagram import circuit_diagram_matplotlib
  f, ax = circuit_diagram_matplotlib(sched)
  # all gates are plotted, but it doesn't all fit in a matplotlib figure
  ax.set_xlim(-.5, 9.5)


Datastructure internals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Let's take a look at the internals of the :class:`~quantify.scheduler.Schedule`.

.. jupyter-execute::

    sched

We can see that the number of unique operations is 24 corresponding to 4 operations that occur in every loop and 21 unique rotations for the different theta angles. (21+4 = 25 so we are missing something.

.. jupyter-execute::

    sched.data.keys()

The schedule consists of a hash table containing all the operations.
This allows efficient loading of pulses or gates to memory and also enables efficient adding of pulse type information as a compilation step.

.. jupyter-execute::

    from pprint import pprint
    from itertools import islice
    # showing the first 5 elements of the operation dict
    pprint(dict(islice(sched.data['operation_dict'].items(), 5)))

The timing constraints are stored as a list of pulses.

.. jupyter-execute::

  sched.data['timing_constraints'][:6]


Similar to the schedule, :class:`~quantify.scheduler.Operation` objects are also based on dicts.

.. jupyter-execute::

    rxy_theta = Rxy(theta=theta, phi=0, qubit=q0)
    pprint(rxy_theta.data)


Compilation of a circuit diagram into pulses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The compilation from the gate-level to the pulse-level description is done using the :ref:`device configuration file<Device configuration file>`.

Here we will use a configuration file for a transmon based system that is part of the quantify-scheduler test suite.

.. jupyter-execute::

  import json
  import pprint
  import os, inspect
  import quantify.scheduler.schemas.examples as es

  esp = inspect.getfile(es)
  cfg_f = os.path.abspath(os.path.join(esp, '..', 'transmon_test_config.json'))


  with open(cfg_f, 'r') as f:
      transmon_test_config = json.load(f)

  pprint.pprint(transmon_test_config)


.. jupyter-execute::

  from quantify.scheduler.compilation import add_pulse_information_transmon, determine_absolute_timing

  add_pulse_information_transmon(sched, device_cfg=transmon_test_config)
  determine_absolute_timing(schedule=sched)


.. jupyter-execute::

  from quantify.scheduler.visualization.pulse_scheme import pulse_diagram_plotly

  pulse_diagram_plotly(sched, port_list=["q0:mw", "q0:res", "q0:fl", "q1:mw"], modulation_if = 10e6, sampling_rate = 1e9)




Compilation of pulses onto physical hardware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. jupyter-execute::
    :hide-code:

    sched = Schedule('Bell experiment')
    for theta in np.linspace(0, 360, 21):
        sched.add(Reset(q0, q1))
        sched.add(X90(q0))
        sched.add(X90(q1), ref_pt='start') # this ensures pulses are aligned
        # sched.add(CZ(q0, q1)) # FIXME Commented out because of not implemented error
        sched.add(Rxy(theta=theta, phi=0, qubit=q0))
        sched.add(Measure(q0, q1), label='M {:.2f} deg'.format(theta))

    add_pulse_information_transmon(sched, device_cfg=transmon_test_config)
    determine_absolute_timing(schedule=sched)

The compilation from the pulse-level description for execution on physical hardware is done using a backend and based on the :ref:`hardware mapping file<Hardware mapping file>`.

Here we will use the :class:`~quantify.scheduler.backends.pulsar_backend.pulsar_assembler_backend` made for the Qblox pulsar series hardware.

.. jupyter-execute::

  import pprint

  cfg_f = os.path.abspath(os.path.join(esp, '..', 'qblox_test_mapping.json'))

  with open(cfg_f, 'r') as f:
      qblox_test_mapping = json.load(f)

  pprint.pprint(qblox_test_mapping)


The Pulsar QCM provides a QCoDeS based Python API. As well as interfacing with real hardware, it provides a mock driver we can use for testing and development, which we will
also use for demonstration purposes as part of this tutorial:


.. jupyter-execute::

  from pulsar_qcm.pulsar_qcm import pulsar_qcm_dummy
  from pulsar_qrm.pulsar_qrm import pulsar_qrm_dummy

  qcm0 = pulsar_qcm_dummy('qcm0')
  qcm1 = pulsar_qcm_dummy('qcm1')
  qrm0 = pulsar_qrm_dummy('qrm0')


.. jupyter-execute::

  from quantify.scheduler.backends.pulsar_backend import pulsar_assembler_backend, configure_pulsars
  from pulsar_qcm.pulsar_qcm import pulsar_qcm
  from qcodes import Instrument

  sched, config = pulsar_assembler_backend(sched, qblox_test_mapping)

The compiled schedule can be uploaded to the hardware using the following command.

.. jupyter-execute::

  configure_pulsars(config, qblox_test_mapping)


At this point, the assembler on the device will load the waveforms into memory and verify the program can be executed. We must next arm and then start the device:


.. jupyter-execute::

     qcm0.arm_sequencer()
     qcm1.arm_sequencer()
     qrm0.arm_sequencer()

     qcm0.start_sequencer()
     qcm1.start_sequencer()
     qrm0.start_sequencer()





Precise timing control: The Ramsey experiment
------------------------------------------------

.. todo::

  This tutorial should showcase in detail the timing options possible in the
  schedule.



A hybrid experiment: The Chevron
------------------------------------------------

As well as defining our schedules in terms of Gates, we can also interleave arbitrary Pulse shapes, or even define a
schedule entirely with Pulses. This can be useful for experiments involving pulse sequences not easily represented by
Gates, such as the Chevron experiment. In this experiment, we want to vary the length and amplitude of a square pulse
between X gates on a pair of qubits.


.. jupyter-execute::

    from quantify.scheduler.gate_library import X, X90, Reset, Measure
    from quantify.scheduler.pulse_library import SquarePulse
    from quantify.scheduler.resources import ClockResource

    sched = Schedule("Chevron Experiment")
    for duration in np.linspace(20e-9, 40e-9, 5):
        for amp in np.linspace(0.1, 1.0, 10):
            begin = sched.add(Reset('q0', 'q1'))
            sched.add(X('q0'), ref_op=begin, ref_pt='start')
            # NB we specify a clock for tutorial purposes,
            # Chevron experiments do not necessarily use modulated square pulses
            square = sched.add(SquarePulse(amp, duration, 'q0:mw', clock="q0.01"))
            sched.add(X90('q0'), ref_op=square)
            sched.add(X90('q1'), ref_op=square)
            sched.add(Measure('q0', 'q1'))
    sched.add_resources([ClockResource("q0.01", 6.02e9)])  # manually add the pulse clock


Note that we add Pulses using the same interface as Gates. Pulses are Operations, and as such support the same timing
and reference operators as Gates.

.. warning::

    When adding a Pulse to a schedule, the clock is not automatically added to the resources of the schedule. It may
    be necessary to add this clock manually, as in the final line of the above example

We can also quickly compile using the :func:`!qcompile` function and associate mapping files:

.. jupyter-execute::

    from quantify.scheduler.compilation import qcompile
    sched, cfg = qcompile(sched, transmon_test_config, qblox_test_mapping)

.. seealso::

    The complete source code of this tutorial can be found in

    :jupyter-download:notebook:`Tutorial 1. Basic experiment`

    :jupyter-download:script:`Tutorial 1. Basic experiment`
