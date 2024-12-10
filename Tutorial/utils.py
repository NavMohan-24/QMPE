from qutip import Qobj
import numpy as np

def qobj_to_latex(qobj):
    """
    Convert a Qobj (Quantum object from QuTiP) into a LaTeX-compatible matrix representation.

    Parameters:
        qobj (Qobj): The quantum object to be converted.

    Returns:
        str: A LaTeX-compatible string representation of the Qobj.
    """
    if not isinstance(qobj, Qobj):
        raise ValueError("Input must be a Qobj from QuTiP.")
    
    # Get the matrix elements
    data = qobj.full()
    
    # Start the LaTeX string for the matrix
    latex_str = "\\begin{bmatrix}\n"
    
    # Iterate through the matrix and format each row
    for row in data:
        row_str = " & ".join(f"{val:.4g}" for val in row)
        latex_str += row_str + " \\\\\n"
    
    # Close the LaTeX matrix
    latex_str += "\\end{bmatrix}"
    
    return latex_str


def process_qobjs(qobj_list, tol=1e-8):
    """
    Processes a list of numbers or Qobjs by removing negligible complex values
    and setting small real values to zero.

    Parameters:
        qobj_list (list): A list of Qobj objects or real/complex numbers.
        tol (float): Tolerance level for filtering small values (default: 1e-8).

    Returns:
        list: Processed list with values adjusted as per the tolerance.
    """
    
    def process_value(val):
        # Check if the value is complex
        if isinstance(val, complex):
            # Set imaginary part to zero if below tolerance
            val = val.real if abs(val.imag) < tol else val
        # Set real part to zero if below tolerance
        return 0 if abs(val.real) < tol else val

    def process_qobj(qobj):
        # Process each element in the Qobj matrix
        data = qobj.full()  # Get full numpy array of Qobj data
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                data[i, j] = process_value(data[i, j])  # Process each matrix element
        return Qobj(data)  # Return the processed Qobj

    # Check if the list contains Qobj instances
    if all(isinstance(item, Qobj) for item in qobj_list):
        return [process_qobj(qobj) for qobj in qobj_list]
    else:
        # If it's a list of numbers, apply processing to each element
        return [process_value(val) for val in qobj_list]
