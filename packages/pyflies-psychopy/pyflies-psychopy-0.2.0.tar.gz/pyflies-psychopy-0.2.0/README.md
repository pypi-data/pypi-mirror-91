# pyflies-psychopy

Generator for [PsychoPy](https://www.psychopy.org/) experiments from
[pyFlies](https://github.com/pyflies/pyflies) models.

When this project is installed you will have a textX registered generator that
can generate PsychoPy experiment from pyFlies models (`.pf` files). You can
verify that generator is available by:

```
textx list-generators
```

and you can generate PsychoPy experiment by:

```
textx generate <your pyflies model.pf> --target psychopy --overwrite
```

For the details see [running generators
section](https://pyflies.github.io/pyflies/latest/generators/) of pyFlies
documentation.


# Configuration

PsychoPy can be configured in [userPrefs.cfg
file](https://www.psychopy.org/general/prefs.html#preferences). Its location
[varies by
machine](https://www.psychopy.org/troubleshooting.html#cleaning-preferences-and-app-data).

You can use `Preferences` dialog in the PsychoPy GUI for the configuration.


# Parameters in the `target` configuration block

See `pfpsychopy.default_settings`.

- `resolution: Point` - Screen/window resolution, default is `(1024, 768)`
- `fullScreen: boolean` - should the experiment run in full screen, default is `false`
- `background: string` - background color, default is `black`
- `frameTolerance` - tolerance in frame duration in seconds, default is `0.001`


# Credits

Initial project layout generated with `textx startproject`.
