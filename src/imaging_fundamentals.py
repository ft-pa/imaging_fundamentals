import os
import itertools
import numpy as np

from typing import Union

from scipy.sparse import coo_array

"""
########################################################################
#####################		FUNCTIONS		############################
########################################################################
"""

def toeplitz_from_vector(input_row_vec:Union[list,
                                             tuple,
										     np.ndarray],
						 input_col_vec:Union[list,
						                     tuple,
									         np.ndarray,
									         None] = None,
                         dims:Union[list, tuple, None] = None,
						 is_conv:bool = False,
						 return_sparse:bool = False) -> Union[np.ndarray,
						                                      coo_array]:
	"""
	Returns a Toeplitz matrix expanded on the entries of
	``input_row_vec`` and, optionally, those from ``input_col_vec``. Can
	be used to generate a convolution matrix by setting``is_conv`` as
	 ``True``

	Parameters
	----------
	input_row_vec: ``list``, ``tuple``, ``numpy.ndarray``
	Input data to be used in the matrix expansion.

	input_col_vec: ``list``, ``tuple``, ``numpy.ndarray``, optional
	(default=``None``)
	Optional data to be used in the matrix expansion, in column-axis.
	When not given, the output matrix will be expanded
	symmetrically over input_row_vec

	dims: ``list``, ``tuple``, optional (default=``None``)
	Dimensions of the output matrix. If it is not given, the output
	matrix will be square, with the numbers of rows and columns equal to
	inputs lengths. Note that setting smaller dimensions will lead to a
	truncated expansion, whereas setting greater dimensions will lead to
	a zero-padded expansion

	return_sparse: ``bool``, optional (default=``False``)
	When set to ``True``, the output is returned as a Scipy sparse
	array in coordinate format. This option is particularly useful when
	``is_conv=True``

	is_conv: ``bool``, optional (default=``False``)
	When set to ``True``, causes the function to return a lower
	triangular Toeplitz matrix. Note that in this case ``input_col_vec``
	is ignored


	Returns
	-------
	toep_mat : ``numpy.ndarray`` or ``coo_array``
	A matrix that is constant along its diagonals. That is, given an
	input vector
	$$
		\mathbf{h} = \begin{bmatrix}
						t_0 & t_1 & \dots t_{N-1}
					 \end{bmatrix},
	$$
	the following matrix is returned:
	$$
		\mathbf{H} =
        \begin{bmatrix}
            t_0     &   t_{-1}   &  t_{-2}   &  \dots & t_{-(N-1)}  \\
            t_1     &   t_0      &  t_{-1}   &  \dots & t_{-N}      \\
            t_2     &   t_1      &  t_0      &  \dots & t_{-N+1}    \\
            t_3     &   t_2      &  t_1      &  \dots & t_{-N+2}    \\
            \vdots  &   \vdots   &  \vdots   &  \ddots & \vdots      \\
            t_{N-1} &   t_{N-2}  &  t_{N-3}  &  \dots & t_{0}
        \end{bmatrix},
	$$
	where entries with negative indexes come either from an auxiliary
	vector (column vector), or from $\mathbf{h}$ itself.

	Depending on the value assigned to ``return_sparse``, the output
	matrix will be either a numpy.ndarray or a scipy.sparse.coo_array
	"""

	"""
	+---------------------------------+
	|   HANDLE row_vec AND col_vec    |
	+---------------------------------+
	"""
	if isinstance(input_row_vec, (list, tuple)):
		rv_type = type(input_row_vec[0])

		row_vec = np.array(input_row_vec,
					       ndmin=1,
					       dtype=rv_type)
	elif isinstance(input_row_vec, np.ndarray):
		rv_type = input_row_vec.dtype

		row_vec = input_row_vec
	else:
		raise TypeError(r"input_row_vec must be array-like")

	if is_conv:
		cv_type = row_vec.dtype

		col_vec = np.zeros_like(row_vec)
		col_vec[0] = row_vec[0]
	else:
		if input_col_vec is None:
			cv_type = row_vec.dtype

			col_vec = row_vec
		elif isinstance(input_col_vec, (list, tuple)):
			cv_type = type(col_vec[0])

			col_vec = np.array(input_col_vec,
							ndmin=1,
							dtype=cv_type)
		elif isinstance(input_col_vec, np.ndarray):
			cv_type = input_col_vec.dtype

			col_vec = input_col_vec
		else:
			str_err = r"col_vec must be array-like"

			raise TypeError(str_err)

		if col_vec[0]!=input_row_vec[0]:
			str_err =  r"input_row_vec and input_col_vec must be "
			str_err += r"equal at [0]"

			raise ValueError(str_err)

	"""
	+-----------------------------+
	|    CONFORM OUTPUT MATRIX    |
	+-----------------------------+
	"""
	if dims is None:
		num_rows = len(row_vec)
		num_cols = len(col_vec)
	else:
		num_rows, num_cols = dims

		if num_rows<len(row_vec):
			row_vec = row_vec[:num_rows]

			num_rows = len(row_vec)
		elif num_rows>len(row_vec):
			row_vec = np.array([*row_vec,
								*np.zeros(num_rows-len(row_vec))],
								dtype=rv_type)

		if num_cols<len(col_vec):
			col_vec = col_vec[:num_cols]

			num_cols = len(col_vec)
		elif num_cols>len(col_vec):
			col_vec = np.array([*col_vec,
								*np.zeros(num_cols-len(col_vec))],
								dtype=cv_type)

	if rv_type==cv_type:
		output_type = rv_type
	else:
		output_type = np.float64

	toep_mat = np.zeros((num_rows, num_cols),
	                    dtype=output_type)

	iter_ji = itertools.product(np.r_[0:num_cols],
                                np.r_[0:num_rows])

	for ji in iter_ji:
		i, j = ji[-1::-1]

		k = i-j

		if k>=0:
			toep_mat[i, j] = row_vec[k]
		else:
			toep_mat[i, j] = col_vec[-k]

	if return_sparse:
		toep_mat = coo_array(toep_mat,
		                     dtype=output_type)

	return toep_mat



