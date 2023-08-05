/*
 * Python object definition of the sequence and iterator object of partitions
 *
 * Copyright (C) 2019-2021, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _PYVSGPT_PARTITIONS_H )
#define _PYVSGPT_PARTITIONS_H

#include <common.h>
#include <types.h>

#include "pyvsgpt_libvsgpt.h"
#include "pyvsgpt_python.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct pyvsgpt_partitions pyvsgpt_partitions_t;

struct pyvsgpt_partitions
{
	/* Python object initialization
	 */
	PyObject_HEAD

	/* The parent object
	 */
	PyObject *parent_object;

	/* The get item by index callback function
	 */
	PyObject* (*get_item_by_index)(
	             PyObject *parent_object,
	             int index );

	/* The current index
	 */
	int current_index;

	/* The number of items
	 */
	int number_of_items;
};

extern PyTypeObject pyvsgpt_partitions_type_object;

PyObject *pyvsgpt_partitions_new(
           PyObject *parent_object,
           PyObject* (*get_item_by_index)(
                        PyObject *parent_object,
                        int index ),
           int number_of_items );

int pyvsgpt_partitions_init(
     pyvsgpt_partitions_t *sequence_object );

void pyvsgpt_partitions_free(
      pyvsgpt_partitions_t *sequence_object );

Py_ssize_t pyvsgpt_partitions_len(
            pyvsgpt_partitions_t *sequence_object );

PyObject *pyvsgpt_partitions_getitem(
           pyvsgpt_partitions_t *sequence_object,
           Py_ssize_t item_index );

PyObject *pyvsgpt_partitions_iter(
           pyvsgpt_partitions_t *sequence_object );

PyObject *pyvsgpt_partitions_iternext(
           pyvsgpt_partitions_t *sequence_object );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _PYVSGPT_PARTITIONS_H ) */

