# `managed/`

Engine-provided state values, not normal application state. `base.py` defines/probes managed values; `is_last_step.py` supplies last-step and remaining-step managers. The graph compiler injects these when relevant.
