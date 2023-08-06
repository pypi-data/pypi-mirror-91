"""Library of Hamiltonian functions."""

import numpy as np

hamiltonians = dict()
def hamiltonian_reg_deco(func):
    """
    Decorator for making registry of functions
    """
    hamiltonians[str(func.__name__)] = func
    return func

@hamiltonian_reg_deco
def resonator(a):
    """
    Harmonic oscillator hamiltonian given the annihilation operator.

    Parameters
    ----------
    a : Tensor
        Annihilator.

    Returns
    -------
    Tensor
        Number operator.

    """
    a_dag = a.T.conj()
    return np.matmul(a_dag, a)

@hamiltonian_reg_deco
def duffing(a):
    """
    Anharmonic part of the duffing oscillator.

    Parameters
    ----------
    a : Tensor
        Annihilator.

    Returns
    -------
    Tensor
        Number operator.

    """
    a_dag = a.T.conj()
    n = np.matmul(a_dag, a)
    return 1/2 * np.matmul(n - np.eye(int(n.shape[0]), dtype=np.complex128), n)

@hamiltonian_reg_deco
def int_XX(anhs):
    """
    Dipole type coupling.

    Parameters
    ----------
    anhs : Tensor list
        Annihilators.

    Returns
    -------
    Tensor
        coupling

    """
    a = anhs[0]
    b = anhs[1]
    a_dag = a.T.conj()
    b_dag = b.T.conj()
    return np.matmul(a_dag + a, b_dag + b)

@hamiltonian_reg_deco
def int_YY(anhs):
    """
    Dipole type coupling.

    Parameters
    ----------
    anhs : Tensor list
        Annihilators.

    Returns
    -------
    Tensor
        coupling

    """
    a = anhs[0]
    b = anhs[1]
    a_dag = a.T.conj()
    b_dag = b.T.conj()
    return -np.matmul(a_dag - a, b_dag - b)

@hamiltonian_reg_deco
def x_drive(a):
    """
    Semiclassical drive.

    Parameters
    ----------
    a : Tensor
        Annihilator.

    Returns
    -------
    Tensor
        Number operator.

    """
    a_dag = a.T.conj()
    return a_dag + a

@hamiltonian_reg_deco
def y_drive(a):
    """
    Semiclassical drive.

    Parameters
    ----------
    a : Tensor
        Annihilator.

    Returns
    -------
    Tensor
        Number operator.

    """
    a_dag = a.T.conj()
    return 1.0j * (a_dag - a)

@hamiltonian_reg_deco
def z_drive(a):
    """
    Semiclassical drive.

    Parameters
    ----------
    a : Tensor
        Annihilator.

    Returns
    -------
    Tensor
        Number operator.

    """
    a_dag = a.T.conj()
    return np.matmul(a_dag, a)
