.. _statistics:

#################
Sample Statistics
#################

After filtering, you can calculated and export integrated compositional values for your analyses:

.. literalinclude:: ../../../../tests/test_beginnersGuide.py
   :language: python
   :dedent: 4
   :lines: 56

Where ``stats`` specifies which functions you would like to use to calculate the statistics.
Built in options are:

* ``'mean'``: Arithmetic mean, calculated by ``np.nanmean``.
* ``'std'``: Arithmetic standard deviation, calculated by ``np.nanstd``.
* ``'se'``:  Arithmetic standard error, calculated by ``np.nanstd / n``.
* ``'H15_mean'``: Huber (H15) robust mean.
* ``'H15_std'``: Huber (H15) robust standard deviation.
* ``'H15_se'``: Huber (H15) robust standard error.
* ``custom_fn(a)``: A function you've written yourself, which takes an array (``a``) and returns a single value. This function must be able to cope with ``NaN`` values.

Where the Huber (H15) robust statistics remove outliers from the data, as described `here <http://www.rsc.org/images/robust-statistics-technical-brief-6_tcm18-214850.pdf>`_.

You can specify any function that accepts an array and returns a single value here.
``filt`` can either be True (applies all active filters), or a specific filter number or partially matching name to apply a specific filter.
In combination with data subsets, and the ability to specify different combinations of filters for different subsets, this provides a flexible way to explore the impact of different filters on your integrated values.

We've now calculated the statistics, but they are still trapped inside the 'analyse' data object (``eg``).
To get them out into a more useful form:

.. literalinclude:: ../../../../tests/test_beginnersGuide.py
   :language: python
   :dedent: 4
   :lines: 58

This returns a :class:`pandas.DataFrame` containing all the statistics we just calculated.
You can either keep this data in python and continue your analysis, or export the integrated values to an external file for analysis and plotting in *your_favourite_program*.

The calculated statistics are saved autoatmically to 'sample_stats.csv' in the 'data_export' directory. 
You can also specify the filename manually using the ``filename`` variable in :meth:`~latools.analyse.getstats`, which will be saved in the 'data_export' directory, or you can use the pandas built in export methods like :meth:`~pandas.DataFrame.to_csv` or :meth:`~pandas.DataFrame.to_excel` to take your data straight to a variety of formats, for example::

	stats.to_csv('stats.csv') # .csv format
