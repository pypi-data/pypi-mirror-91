import warnings

from secedgar.client.network_client import NetworkClient
from secedgar.utils.cik_map import get_cik_map
from secedgar.utils.exceptions import CIKError, EDGARQueryError


class _CIKValidator(object):
    """Validates company tickers and/or company names based on CIK availability.

    Used internally by the CIK class. Not intended for outside use.

    Args:
        lookups (Union[str, list, tuple]): List of tickers and/or company names for
            which to find CIKs.
        **kwargs: Any kwargs will be passed to NetworkClient if no client is given.

    .. versionadded:: 0.1.5
    """

    # See Stack Overflow's answer to how-do-you-pep-8-name-a-class-whose-name-is-an-acronym
    # if you are wondering whether CIK should be capitalized in the class name or not.
    def __init__(self, lookups, client=None, **kwargs):
        # Make sure lookups is not empty string
        if lookups and isinstance(lookups, str):
            self._lookups = [lookups]  # make single string into list
        else:
            # Check that iterable only contains strings and is not empty
            if not (lookups and all(type(o) is str for o in lookups)):
                raise TypeError("CIKs must be given as string or iterable.")
            self._lookups = lookups
        self._params = {'action': 'getcompany'}
        self._client = client if client is not None else NetworkClient(**kwargs)

    @property
    def path(self):
        """str: Path to add to client base."""
        return "cgi-bin/browse-edgar"

    @property
    def client(self):
        """``secedgar.client_.base``: Client to use to fetch requests."""
        return self._client

    @property
    def params(self):
        """:obj:`dict` Search parameters to add to client."""
        return self._params

    @property
    def lookups(self):
        """`list` of `str` to lookup (to get CIK values)."""
        return self._lookups

    def get_ciks(self):
        """Validate lookup values and return corresponding CIKs.

        Returns:
            ciks (dict): Dictionary with lookup terms as keys and CIKs as values.

        """
        ciks = dict()
        to_lookup = set(self.lookups)
        found = set()

        # First, try to get all CIKs with ticker map
        # Tickers in map are upper case, so look up with upper case
        ticker_map = get_cik_map(key="ticker")
        for lookup in to_lookup:
            try:
                ciks[lookup] = ticker_map[lookup.upper()]
                found.add(lookup)
            except KeyError:
                continue
        to_lookup -= found

        # If any more lookups remain, try to finish with company name map
        # Case varies from company, so lookup with what is given
        if to_lookup:
            company_map = get_cik_map(key="title")
            for lookup in to_lookup:
                try:
                    ciks[lookup] = company_map[lookup]
                    found.add(lookup)
                except KeyError:
                    continue
            to_lookup -= found

        # Finally, if lookups are still left, look them up through the SEC's search
        for lookup in to_lookup:
            try:
                result = self._get_cik(lookup)
                self._validate_cik(result)  # raises error if not valid CIK
                ciks[lookup] = result
            except CIKError:
                pass  # If multiple companies, found, just print out warnings
        return ciks

    # TODO: Add mock to test this functionality
    def _get_lookup_soup(self, lookup):
        """Gets `BeautifulSoup` object for lookup.

        First tries to lookup using CIK. Then falls back to company name.

        .. warning::
           Only to be used internally by `_get_cik` to get CIK from lookup.

        Args:
            lookup (str): CIK, company name, or ticker symbol to lookup.

        Returns:
            soup (bs4.BeautifulSoup): `BeautifulSoup` object to be used to get
                company CIK.
        """
        try:  # try to lookup by CIK
            self._params['CIK'] = lookup
            return self._client.get_soup(self.path, self.params)
        except EDGARQueryError:  # fallback to lookup by company name
            self.params.pop('CIK')  # delete this parameter so no conflicts arise
            self._params['company'] = lookup
            return self._client.get_soup(self.path, self.params)

    def _get_cik(self, lookup):
        """Gets CIK from `BeautifulSoup` object.

        .. warning: This method will warn when lookup returns multiple possibilities for a
            CIK are found.

        Args:
            lookup (str): CIK, company name, or ticker symbol which was looked up.

        Returns:
            CIK (str): CIK for lookup.
        """
        self._validate_lookup(lookup)
        soup = self._get_lookup_soup(lookup)
        try:  # try to get single CIK for lookup
            span = soup.find('span', {'class': 'companyName'})
            return span.find('a').getText().split()[0]  # returns single CIK
        except AttributeError:  # warn and skip if multiple possibilities for CIK found
            warning_message = """Lookup '{0}' will be skipped.
                          Found multiple companies matching '{0}':
                          {1}""".format(lookup, '\n'.join(self._get_cik_possibilities(soup)))
            warnings.warn(warning_message)
        finally:
            # Delete parameters after lookup
            self.params.pop('company', None)
            self.params.pop('CIK', None)

    @staticmethod
    def _get_cik_possibilities(soup):
        """Get all CIK possibilities if multiple are listed.

        Args:
            soup (BeautifulSoup): BeautifulSoup object to search through.

        Returns:
            All possible companies that match lookup.
        """
        try:
            # Exclude table header
            table_rows = soup.find('table', {'summary': 'Results'}).find_all('tr')[1:]
            # Company names are in second column of table
            return [''.join(row.find_all('td')[1].find_all(text=True)) for row in table_rows]
        except AttributeError:
            # If there are no CIK possibilities, then no results were returned
            raise EDGARQueryError

    @staticmethod
    def _validate_cik(cik):
        """Check if CIK is 10 digit string."""
        if not (isinstance(cik, str) and len(cik) == 10 and cik.isdigit()):
            raise CIKError(cik)

    @staticmethod
    def _validate_lookup(lookup):
        """Ensure that lookup is string.

        Args:
            lookup: Value to lookup.

        Raises:
            TypeError: If lookup is not a non-empty string.
        """
        if not (lookup and isinstance(lookup, str)):
            raise TypeError("Lookup value must be string. Given type {0}.".format(type(lookup)))
