# You must define an inputs object
from pyfecons.Inputs import Inputs


def Generate():
    return Inputs(
        Inputs.CustomerInfo(name="Clean Air Task Force"),
        Inputs.Basic(
            time_to_replace=10,
            down_time=10,
            reactor_type=2,
            n_mod=1,
            am=1,
            construction_time=3
        ),
        Inputs.Blanket(
            first_wall=1,
            blanket_type=0,
            primary_coolant=0,
            secondary_coolant=7,
            neutron_multiplier=3,
            structure=1
        )
    )
