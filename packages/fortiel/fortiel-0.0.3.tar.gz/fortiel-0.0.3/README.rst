
fortiel - Fortran preprocessor and metaprogramming engine
=========================================================

Fortiel is a Fortran preprocessor. 

Installation
============

Fortiel can be install as the `PyPI package <https://pypi.org/project/fortiel/>`_\ :

.. code-block:: bash

   pip3 install fortiel

Preprocessor language
=====================

Directives
----------

Common directive syntax is:

.. code-block:: fortran

   #fpp <directive> <directiveArguments>

where ``<directive>`` is one of the known preprocessor directives.
Both ``fpp`` and ``<directive>`` are case-insensitive.

``let`` directive
^^^^^^^^^^^^^^^^^^^^^

``let`` directive declares a new named variable.

**Syntax**\ :

.. code-block:: fortran

   #fpp let <var> = <expression>

``<expression>`` should be a valid Python 3 expression, 
that may refer to the previously defined variables, Fortiel builtins and
Python 3 builtins.

Functions can be also declared using the ``let`` directive.

**Syntax**

.. code-block:: fortran

   #fpp let <var>([<argument>[, <anotherArgument>]*]) = <expression>

``undef`` directive
^^^^^^^^^^^^^^^^^^^^^^^

``undef`` directive undefines the names, previously defined
with the ``let`` directive. 

**Syntax**\ :

.. code-block:: fortran

   #fpp undef <var>[, <anotherVar>]*

Builtin names like ``__FILE__`` or ``__LINE__`` can not be undefined.

``if``\ /\ ``else if``\ /\ ``else``\ /\ ``end if`` directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``if`` is a classic conditional directive.

**Syntax**\ :

.. code-block:: fortran

   #fpp if <condition>
     ! Fortran code.
   #fpp else if <condition>
     ! Fortran code.
   #fpp else
     ! Fortran code.
   #fpp end if

Note that ``else if`` and ``elseif`` directives, 
``end if`` and ``endif`` directives are equivalent.

``do``\ /\ ``end do`` directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``do`` directives substitutes the code multiple times.

**Syntax**\ :

.. code-block:: fortran

   #fpp do <var> = <first>, <last>[, <step>]
     ! Fortran code.
   #fpp end do

``<first>``\ , ``<last>`` and optional ``<step>`` expressions should 
evaluate to integers.
Inside the loop body a special variable ``__INDEX__`` is defined,
which is equal to the the current iterator value.

Note that ``end do`` and ``enddo`` directives are equivalent.

``include`` and ``use`` directives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``include`` directive directly includes the
contents of the file located at ``<filePath>`` into the current source.

**Syntax**\ :

.. code-block:: fortran

   #fpp include '<filePath>'
   ! or
   #fpp include "<filePath>"
   ! or
   #fpp include <<filePath>>

``use`` directive is the same as ``include``\ , but it skips the
non-directive lines. 

**Syntax**\ :

.. code-block:: fortran

   #fpp use <filePath>
   ! or
   #fpp use <filePath>
   ! or
   #fpp use <<filePath>>

``line`` directive
^^^^^^^^^^^^^^^^^^^^^^

``line`` directive changes current line number and file path.

**Syntax**\ :

.. code-block:: fortran

   #fpp [line] <lineNumber> "<filePath>"

In-line substitutions
---------------------

``{}`` substitution
^^^^^^^^^^^^^^^^^^^^^^^

``@:`` substitution
^^^^^^^^^^^^^^^^^^^^^^^

Examples
========

Generic programming
-------------------

.. code-block:: fortran

   module Distances

     implicit none

     #fpp let NUM_RANKS = 2

     interface computeSquareDistance
     #fpp do rank = 0, NUM_RANKS
       module procedure computeSquareDistance{rank}
     #fpp end do    
     end interface computeSquareDistance

   contains

   #fpp do rank = 0, NUM_RANKS
     function computeSquareDistance{rank}(n, u, v) result(d)
       integer, intent(in) :: n
       real, intent(in) :: u(@:,:), v(@:,:)
       real :: d
       integer :: i
       d = 0.0
       do i = 1, n
       #fpp if rank == 0
         d = d + (u(i) - v(i))**2
       #fpp else
         d = d + sum((u(@:,i) - v(@:,i))**2)
       #fpp end if
       end do
     end function computeSquareDistance{rank}
   #fpp end do    
   end module Distances

.. code-block:: fortran

   module Distances

     implicit none

     interface computeSquareDistance
       module procedure computeSquareDistance0
       module procedure computeSquareDistance1
       module procedure computeSquareDistance2
     end interface computeSquareDistance

   contains

     function computeSquareDistance0(n, u, v) result(d)
       integer, intent(in) :: n
       real, intent(in) :: u(:), v(:)
       real :: d
       integer :: i
       d = 0.0
       do i = 1, n
         d = d + (u(i) - v(i))**2
       end do
     end function computeSquareDistance0
     function computeSquareDistance1(n, u, v) result(d)
       integer, intent(in) :: n
       real, intent(in) :: u(:,:), v(:,:)
       real :: d
       integer :: i
       d = 0.0
       do i = 1, n
         d = d + sum((u(:,i) - v(:,i))**2)
       end do
     end function computeSquareDistance1
     function computeSquareDistance2(n, u, v) result(d)
       integer, intent(in) :: n
       real, intent(in) :: u(:,:,:), v(:,:,:)
       real :: d
       integer :: i
       d = 0.0
       do i = 1, n
         d = d + sum((u(:,:,i) - v(:,:,i))**2)
       end do
     end function computeSquareDistance2
   end module Distances

Missing features
================
