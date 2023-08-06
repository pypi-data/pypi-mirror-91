:orphan:

:mod:`cloup._option_groups`
===========================

.. py:module:: cloup._option_groups





                              

Classes summary
---------------

.. autosummary::

   cloup._option_groups.OptionGroup
   cloup._option_groups.GroupedOption

Functions Summary
-----------------

.. autosummary::

   cloup._option_groups.has_option_group
   cloup._option_groups.get_option_group_of
   cloup._option_groups.option
   cloup._option_groups.option_group


                                           
Contents
--------
.. data:: OptionDecorator
   

   

.. py:class:: OptionGroup(name: str, help: Optional[str] = None)

   .. method:: get_help_records(self, ctx: click.Context)


   .. method:: option(self, *param_decls, **attrs)


   .. method:: __iter__(self)


   .. method:: __getitem__(self, i: int) -> click.Option


   .. method:: __len__(self) -> int


   .. method:: __repr__(self) -> str

      Return repr(self).


   .. method:: __str__(self) -> str

      Return str(self).



.. py:class:: GroupedOption(*args, group: Optional[OptionGroup] = None, **attrs)

   Bases: :class:`click.Option`

   A click.Option with an extra field ``group`` of type OptionGroup 


.. function:: has_option_group(param) -> bool


.. function:: get_option_group_of(param, default=None)


.. function:: option(*param_decls, group: Optional[OptionGroup] = None, cls: Type[click.Option] = GroupedOption, **attrs) -> OptionDecorator


.. function:: option_group(name: str, help: str, *options) -> OptionDecorator
              option_group(name: str, *options, help: Optional[str] = None) -> OptionDecorator

   Attaches an option group to the command. This decorator is overloaded with
   two signatures::

       @option_group(name: str, *options, help: Optional[str] = None)
       @option_group(name: str, help: str, *options)

   In other words, if the second position argument is a string, it is interpreted
   as the "help" argument. Otherwise, it is interpreted as the first option;
   in this case, you can still pass the help as keyword argument.



                                         