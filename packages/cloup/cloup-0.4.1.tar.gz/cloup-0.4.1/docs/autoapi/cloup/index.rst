
:mod:`cloup`
============

.. py:module:: cloup

.. autoapi-nested-parse::

   Top-level package for cloup.





                              

Classes summary
---------------

.. autosummary::

   cloup.GroupedOption
   cloup.OptionGroup
   cloup.Command
   cloup.Group
   cloup.GroupSection

Functions Summary
-----------------

.. autosummary::

   cloup.option
   cloup.option_group
   cloup.command
   cloup.group


                                           
Contents
--------
.. data:: __author__
   :annotation: = Gianluca Gippetto

   

.. data:: __email__
   :annotation: = gianluca.gippetto@gmail.com

   

.. data:: __version__
   :annotation: = 0.4.1

   

.. py:class:: GroupedOption(*args, group: Optional[OptionGroup] = None, **attrs)

   Bases: :class:`click.Option`

   A click.Option with an extra field ``group`` of type OptionGroup 


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


.. py:class:: Command(name, context_settings=None, callback=None, params=None, help=None, epilog=None, short_help=None, options_metavar='[OPTIONS]', add_help_option=True, hidden=False, deprecated=False, align_option_groups=True, **kwargs)

   Bases: :class:`click.Command`

   A ``click.Command`` supporting option groups. 

   .. method:: get_ungrouped_options(self, ctx: click.Context) -> Sequence[click.Option]


   .. method:: format_option_group(self, ctx: click.Context, formatter: click.HelpFormatter, option_group: OptionGroup, help_records: Optional[Sequence] = None)


   .. method:: format_options(self, ctx: click.Context, formatter: click.HelpFormatter, max_option_width: int = 30)

      Writes all the options into the formatter if they exist.



.. py:class:: Group(name: Optional[str] = None, commands: Optional[Dict[str, click.Command]] = None, sections: Iterable[GroupSection] = (), align_sections: bool = True, **attrs)

   Bases: :class:`click.Group`

   A ``click.Group`` that supports subcommand help sections and returns
   and whose subcommands are, by default, of class ``cloup.Commands``.

   Subgroups can be specified in different ways:

   #. just pass a list of GroupSection objects to the constructor in ``sections``
   #. use ``add_section`` to add a section
   #. use ``add_command(cmd, name, section, ...)``
   #. use ``group.command(name, section, ...)``

   Commands not included in any user-defined section are added to the
   "default section", whose title is "Commands" or "Other commands" depending
   on whether it is the only section or not. The default section is the last
   shown section in the help and its commands are listed in lexicographic order.

   .. method:: command(self, name: Optional[str] = None, section: Optional[GroupSection] = None, cls: Type[click.Command] = Command, **attrs) -> Callable[[Callable], click.Command]

      Creates a new command and adds it to this group. 


   .. method:: group(self, name: Optional[str] = None, section: Optional[GroupSection] = None, cls: Optional[Type[click.Group]] = None, **attrs) -> Callable[[Callable], click.Group]

      A shortcut decorator for declaring and attaching a group to
      the group.  This takes the same arguments as :func:`group` but
      immediately registers the created command with this instance by
      calling into :meth:`add_command`.


   .. method:: add_section(self, section: GroupSection)

      Adds a :class:`GroupSection` to this group. You can add the same
      section object a single time. 


   .. method:: section(self, title: str, *commands: click.Command, **attrs) -> GroupSection

      Creates a new :class:`GroupSection`, adds it to this group and returns it. 


   .. method:: add_command(self, cmd: click.Command, name: Optional[str] = None, section: Optional[GroupSection] = None)

      Adds a new command. If ``section`` is None, the command is added to the default section.


   .. method:: list_sections(self, ctx: click.Context, include_default_section: bool = True) -> List[GroupSection]

      Returns the list of all sections in the "correct order".
      if ``include_default_section=True`` and the default section is non-empty,
      it will be included at the end of the list. 


   .. method:: format_commands(self, ctx: click.Context, formatter: click.HelpFormatter)

      Extra format methods for multi methods that adds all the commands
      after the options.


   .. method:: format_section(self, ctx: click.Context, formatter: click.HelpFormatter, section: GroupSection, command_col_width: Optional[int] = None)



.. py:class:: GroupSection(title: str, commands: Subcommands = (), sorted: bool = False)

   A section of commands inside a ``cloup.Group``. Sections are not
   (multi)commands, they simply allow to organize cloup.Group subcommands
   in many different help sections.

   .. method:: sorted(cls, title: str, commands: Subcommands = ()) -> 'GroupSection'
      :classmethod:


   .. method:: add_command(self, cmd: click.Command, name: Optional[str] = None)


   .. method:: list_commands(self) -> List[Tuple[str, click.Command]]


   .. method:: __len__(self) -> int


   .. method:: __repr__(self) -> str

      Return repr(self).



.. function:: command(name: Optional[str] = None, cls: Type[Command] = Command, **attrs) -> Callable[[Callable], Command]

   Creates a new ``cloup.Command`` (by default). 


.. function:: group(name: Optional[str] = None, cls: Type[Group] = Group, **attrs) -> Callable[[Callable], Group]

   Creates a new ``Group`` (by default). 



                                         