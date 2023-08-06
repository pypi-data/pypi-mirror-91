from falcon_client.utils import callersname


class PreventionPoliciesMixin:
    def prevention_policies_search(self, offset=0, limit=5000, sort='name.asc', fql_filter=None,
                                   api_endpoint='/policy/queries/prevention/v1'):
        """
        Search for Prevention Policies in your environment by providing an FQL filter and paging details.
        Returns a set of Prevention Policy IDs which match the filter criteria.
        :param offset: The offset to page from, for the next result set
        :param limit: The maximum records to return. [1-5000]
        :param sort: The property to sort by (e.g. status.desc or hostname.asc)
        :param fql_filter: The Falcon Query Language filter expression that should be used to limit the results
        :param api_endpoint: see https://assets.falcon.crowdstrike.com/support/api/swagger.html#/
        :return: generator obj containing list of Prevention policy IDs.
        """
        try:
            r_params = {'offset': offset, 'limit': limit, 'sort': sort, 'filter': fql_filter}
            _resp = self.api_query(api_endpoint, r_params)
        except Exception as err:
            self.logger.error("Failed to %s.  %s" % (__name__, err))
        else:
            try:
                # Print total results only once
                if callersname() != self.device_search.__name__:
                    self.logger.debug("Filter '%s' returned %d results"
                                      % (fql_filter, _resp.meta['pagination']['total']))
            except:
                pass

            if _resp.success:
                try:
                    offset = _resp.meta['pagination']['offset']
                    total = _resp.meta['pagination']['total']
                except:
                    offset = ""
                else:
                    if len(_resp.data) > 0:
                        yield _resp.data
                finally:
                    r_params['offset'] = offset
                    if offset < total:
                        yield from self.prevention_policies_search(offset, limit, sort, fql_filter)
            else:
                raise _resp.errors

    def prevention_policies_details(self, ids=None, api_endpoint='/policy/entities/prevention/v1'):
        """
        Get details on one or more Prevention policies by providing policy IDs.
        :param ids: list of Prevention policy ids
        :param api_endpoint: see https://assets.falcon.crowdstrike.com/support/api/swagger.html#/
        :return: list of Prevention policy details
        """
        if ids is None:
            ids = set()
            for policy_ids in self.prevention_policies_search():
                ids.update(set(policy_ids))

        if len(ids) > 0:
            self.logger.debug("Prevention policy details will be fetched for %d IDs." % len(ids))
            try:
                r_params = {'ids': ids}
                _resp = self.api_query(api_endpoint, r_params)
            except Exception as err:
                self.logger.error("Failed to %s.  %s" % (__name__, err))
                raise
            else:
                if _resp.success:
                    return _resp.data
                else:
                    raise _resp.errors
