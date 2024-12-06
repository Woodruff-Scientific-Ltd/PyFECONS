import numpy as np
import matplotlib.pyplot as plt


def Scurve(
    k=0.2,
    Csat=100,
    tau_life=40,
    tau_trans=50,
    r=0.05,
    plot=False,
    discount=True,
    time_horizon=150,
    **kwargs
):
    fidelity = time_horizon
    time = np.linspace(0, time_horizon, fidelity)
    if not plot:
        pass
    elif plot and ("fig" not in kwargs and "axs" not in kwargs):
        fig, axs = plt.subplots(1, 2)
    else:
        fig, axs = kwargs["fig"], kwargs["axs"]
    N = np.zeros(fidelity)
    C = np.zeros(fidelity)

    # boundary condition: assume smooth change in capacity at Csat i.e. capacity after saturation time is same as capacity as exponentially scaling capacity at saturation time
    A = Csat * (1.0 / (np.exp(tau_trans * k) - 1))

    if tau_life > tau_trans:
        # first period
        t = (time >= 0) & (time < tau_trans)
        C[t] = A * (np.exp(k * time[t]) - 1)
        N[t] = (A / k) * (np.exp(k * time[t]) - k * time[t] - 1)
        if discount:
            N[t] *= (1 + r) ** -time[t]

        if plot:
            axs[0].plot(time[t], N[t], "r")
            axs[1].plot(time[t], C[t], "r")
        # second period
        t = (time >= tau_trans) & (time < tau_life)
        C[t] = Csat
        N[t] = Csat * (time[t] - tau_trans) + (A / k) * (
            np.exp(k * tau_trans) - tau_trans * k - 1
        )
        if discount:
            N[t] *= (1 + r) ** -time[t]

        if plot:
            axs[0].plot(time[t], N[t], "b")
            axs[1].plot(time[t], C[t], "b")
        # third period
        t = (time >= tau_life) & (time < tau_life + tau_trans)
        C[t] = Csat
        N[t] = Csat * (time[t] - tau_trans) - (A / k) * (
            np.exp(k * (time[t] - tau_life))
            - np.exp(k * tau_trans)
            - k * (time[t] - tau_life - tau_trans)
        )
        if discount:
            N[t] *= (1 + r) ** -time[t]
        if plot:
            axs[0].plot(time[t], N[t], "g")
            axs[1].plot(time[t], C[t], "g")
        # fourth period
        t = time >= tau_trans + tau_life
        C[t] = Csat
        N[t] = Csat * tau_life
        if discount:
            N[t] *= (1 + r) ** -time[t]
        if plot:
            axs[0].plot(time[t], N[t], "m")
            axs[1].plot(time[t], C[t], "m")
    else:
        # first period
        t = (time >= 0) & (time < tau_life)
        C[t] = A * (np.exp(k * time[t]) - 1)
        N[t] = (A / k) * (np.exp(k * time[t]) - k * time[t] - 1)
        if discount:
            N[t] *= (1 + r) ** -time[t]
        if plot:
            axs[0].plot(time[t], N[t], "r")
            axs[1].plot(time[t], C[t], "r")

        # second period
        t = (time >= tau_life) & (time < tau_trans)
        C[t] = A * (np.exp(k * time[t]) - 1)
        N[t] = (A / k) * (
            np.exp(k * time[t]) - np.exp(k * (time[t] - tau_life)) - tau_life * k
        )
        if discount:
            N[t] *= (1 + r) ** -time[t]
        if plot:
            axs[0].plot(time[t], N[t], "b")
            axs[1].plot(time[t], C[t], "b")
        # third period
        t = (time >= tau_trans) & (time < tau_life + tau_trans)
        C[t] = Csat
        N[t] = (A + Csat) * (time[t] - tau_trans) - (A / k) * (
            np.exp(k * (time[t] - tau_life)) - np.exp(k * tau_trans) + tau_life * k
        )
        if discount:
            N[t] *= (1 + r) ** -time[t]
        if plot:
            axs[0].plot(time[t], N[t], "g")
            axs[1].plot(time[t], C[t], "g")
        # fourth period
        t = time >= tau_trans + tau_life
        C[t] = Csat
        N[t] = tau_life * Csat
        if discount:
            N[t] *= (1 + r) ** -time[t]
        if plot:
            axs[0].plot(time[t], N[t], "m")
            axs[1].plot(time[t], C[t], "m")

    if plot and ("fig" not in kwargs and "axs" not in kwargs):
        plt.show()
    else:
        return time, N
