## What and why

<!-- One or two sentences. Link the issue if there is one. -->

## How it was tested

- [ ] `python -m unittest discover -s app -p "test_*.py"` passes
- [ ] `node --test app/*.test.mjs app/test_sim_hand.mjs` passes
- [ ] Tried in the browser (`/sim`, `/sim/camera` or the desk in mock mode)
- [ ] Tried on a real SO-101 (follower / how it was mounted):

## Safety checklist

- [ ] This change does not send motion commands to the arm, or it keeps the existing guards (speed and range limits, stop on lost hand or input, Host/Origin checks)
- [ ] Behavior that was not tested on a real arm or in the browser is marked "unverified"
- [ ] No calibration files, logs, videos, addresses, tokens or photos of a private environment are included
