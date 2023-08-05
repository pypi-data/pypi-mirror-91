/*
 * Library section_values type test program
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

#include <common.h>
#include <file_stream.h>
#include <types.h>

#if defined( HAVE_STDLIB_H ) || defined( WINAPI )
#include <stdlib.h>
#endif

#include "vsgpt_test_libcerror.h"
#include "vsgpt_test_libvsgpt.h"
#include "vsgpt_test_macros.h"
#include "vsgpt_test_memory.h"
#include "vsgpt_test_unused.h"

#include "../libvsgpt/libvsgpt_section_values.h"

#if defined( __GNUC__ ) && !defined( LIBVSGPT_DLL_IMPORT )

/* Tests the libvsgpt_section_values_initialize function
 * Returns 1 if successful or 0 if not
 */
int vsgpt_test_section_values_initialize(
     void )
{
	libcerror_error_t *error                  = NULL;
	libvsgpt_section_values_t *section_values = NULL;
	int result                                = 0;

#if defined( HAVE_VSGPT_TEST_MEMORY )
	int number_of_malloc_fail_tests           = 1;
	int number_of_memset_fail_tests           = 1;
	int test_number                           = 0;
#endif

	/* Test regular cases
	 */
	result = libvsgpt_section_values_initialize(
	          &section_values,
	          &error );

	VSGPT_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	VSGPT_TEST_ASSERT_IS_NOT_NULL(
	 "section_values",
	 section_values );

	VSGPT_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libvsgpt_section_values_free(
	          &section_values,
	          &error );

	VSGPT_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	VSGPT_TEST_ASSERT_IS_NULL(
	 "section_values",
	 section_values );

	VSGPT_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libvsgpt_section_values_initialize(
	          NULL,
	          &error );

	VSGPT_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	VSGPT_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	section_values = (libvsgpt_section_values_t *) 0x12345678UL;

	result = libvsgpt_section_values_initialize(
	          &section_values,
	          &error );

	section_values = NULL;

	VSGPT_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	VSGPT_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

#if defined( HAVE_VSGPT_TEST_MEMORY )

	for( test_number = 0;
	     test_number < number_of_malloc_fail_tests;
	     test_number++ )
	{
		/* Test libvsgpt_section_values_initialize with malloc failing
		 */
		vsgpt_test_malloc_attempts_before_fail = test_number;

		result = libvsgpt_section_values_initialize(
		          &section_values,
		          &error );

		if( vsgpt_test_malloc_attempts_before_fail != -1 )
		{
			vsgpt_test_malloc_attempts_before_fail = -1;

			if( section_values != NULL )
			{
				libvsgpt_section_values_free(
				 &section_values,
				 NULL );
			}
		}
		else
		{
			VSGPT_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			VSGPT_TEST_ASSERT_IS_NULL(
			 "section_values",
			 section_values );

			VSGPT_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
	for( test_number = 0;
	     test_number < number_of_memset_fail_tests;
	     test_number++ )
	{
		/* Test libvsgpt_section_values_initialize with memset failing
		 */
		vsgpt_test_memset_attempts_before_fail = test_number;

		result = libvsgpt_section_values_initialize(
		          &section_values,
		          &error );

		if( vsgpt_test_memset_attempts_before_fail != -1 )
		{
			vsgpt_test_memset_attempts_before_fail = -1;

			if( section_values != NULL )
			{
				libvsgpt_section_values_free(
				 &section_values,
				 NULL );
			}
		}
		else
		{
			VSGPT_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			VSGPT_TEST_ASSERT_IS_NULL(
			 "section_values",
			 section_values );

			VSGPT_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
#endif /* defined( HAVE_VSGPT_TEST_MEMORY ) */

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( section_values != NULL )
	{
		libvsgpt_section_values_free(
		 &section_values,
		 NULL );
	}
	return( 0 );
}

/* Tests the libvsgpt_section_values_free function
 * Returns 1 if successful or 0 if not
 */
int vsgpt_test_section_values_free(
     void )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test error cases
	 */
	result = libvsgpt_section_values_free(
	          NULL,
	          &error );

	VSGPT_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	VSGPT_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

#endif /* defined( __GNUC__ ) && !defined( LIBVSGPT_DLL_IMPORT ) */

/* The main program
 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
int wmain(
     int argc VSGPT_TEST_ATTRIBUTE_UNUSED,
     wchar_t * const argv[] VSGPT_TEST_ATTRIBUTE_UNUSED )
#else
int main(
     int argc VSGPT_TEST_ATTRIBUTE_UNUSED,
     char * const argv[] VSGPT_TEST_ATTRIBUTE_UNUSED )
#endif
{
	VSGPT_TEST_UNREFERENCED_PARAMETER( argc )
	VSGPT_TEST_UNREFERENCED_PARAMETER( argv )

#if defined( __GNUC__ ) && !defined( LIBVSGPT_DLL_IMPORT )

	VSGPT_TEST_RUN(
	 "libvsgpt_section_values_initialize",
	 vsgpt_test_section_values_initialize );

	VSGPT_TEST_RUN(
	 "libvsgpt_section_values_free",
	 vsgpt_test_section_values_free );

#endif /* defined( __GNUC__ ) && !defined( LIBVSGPT_DLL_IMPORT ) */

	return( EXIT_SUCCESS );

on_error:
	return( EXIT_FAILURE );
}

