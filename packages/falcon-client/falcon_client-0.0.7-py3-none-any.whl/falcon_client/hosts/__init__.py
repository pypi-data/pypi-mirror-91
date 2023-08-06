import re
from falcon_client.utils import callersname

aid_re = re.compile(r'(?P<aid>[\w]{32})')


class HostsMixin:
    @staticmethod
    def _chunker(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def device_scroll(self, offset=None, limit=5000, sort='hostname.asc', fql_filter=None,
                      api_endpoint='/devices/queries/devices-scroll/v1'):
        """
        Search for hosts in your environment by platform, hostname, IP, and other criteria with continuous pagination
        capability (based on offset pointer which expires after 2 minutes with no maximum limit)
        :param offset: The offset to page from, for the next result set
        :param limit: The maximum records to return. [1-5000]
        :param sort: The property to sort by (e.g. status.desc or hostname.asc)
        :param fql_filter: The Falcon Query Language filter expression that should be used to limit the results
        :param api_endpoint: see https://assets.falcon.crowdstrike.com/support/api/swagger.html#/
        :return: generator obj containing list of AIDs.
        """
        try:
            r_params = dict({})
            if offset is not None:
                r_params['offset'] = offset
            else:
                r_params = {'limit': limit, 'sort': sort, 'filter': fql_filter}
            _resp = self.api_query(api_endpoint, r_params)
        except Exception as err:
            self.logger.error("Failed to %s.  %s" % (__name__, err))
            raise
        else:
            try:
                # Print total results only once
                if callersname() != self.device_scroll.__name__:
                    self.logger.debug("Filter '%s' returned %d results" % (fql_filter, _resp.meta['pagination']['total']))
            except:
                pass

            if _resp.success:
                try:
                    offset = _resp.meta['pagination']['offset']
                except:
                    offset = ""
                else:
                    if len(_resp.data) > 0:
                        yield _resp.data
                finally:
                    if len(offset) > 0:
                        yield from self.device_scroll(offset)
            else:
                raise _resp.errors

    def device_search(self, offset=0, limit=5000, sort='hostname.asc', fql_filter=None, q=None,
                      api_endpoint='/devices/queries/devices/v1'):
        """
        Search for hosts in your environment by platform, hostname, IP, and other criteria.
        Device Search supports the same options as Device Scroll. The only difference between Device Search and
        Device Scroll is their pagination and response limit:
            Device Search: Standard pagination (page number, page size) up to 150,000 devices
            Device Scroll: Continuous pagination (based on an offset pointer) with no maximum limit
        :param offset: The offset to page from, for the next result set
        :param limit: The maximum records to return. [1-5000]
        :param sort: The property to sort by (e.g. status.desc or hostname.asc)
        :param fql_filter: The Falcon Query Language filter expression that should be used to limit the results
        :param q: Falcon query to search across all FQL fields.
        :param api_endpoint: see https://assets.falcon.crowdstrike.com/support/api/swagger.html#/
        :return: generator obj containing list of AIDs.
        """
        try:
            r_params = {'offset': offset, 'limit': limit, 'sort': sort, 'filter': fql_filter, 'q': q}
            _resp = self.api_query(api_endpoint, r_params)
        except Exception as err:
            self.logger.error("Failed to %s.  %s" % (__name__, err))
        else:
            try:
                # Print total results only once
                if callersname() != self.device_search.__name__:
                    self.logger.debug("Filter '%s' and Query '%s' returned %d results"
                                     % (fql_filter, q, _resp.meta['pagination']['total']))
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
                        yield from self.device_search(offset, limit, sort, fql_filter, q)
            else:
                raise _resp.errors

    def device_details(self, aids=None, batch_size=1000, api_endpoint='/devices/entities/devices/v1', **kwargs):
        """
        Get details on one or more hosts by providing agent IDs (AID).
        :param aids: list of aids
        :param batch_size: Number of host details per API call.
        :param api_endpoint: see https://assets.falcon.crowdstrike.com/support/api/swagger.html#/
        :param kwargs: if aids is none, device scroll will be called if only filter is specified,
                        otherwise device search will be called.
        :return: generator obj containing list of device details
        """
        if aids is None:
            aids = set()
            if 'q' in kwargs.keys():
                for _aid in self.device_search(**kwargs):
                    aids.update(_aid)
            elif 'fql_filter' in kwargs.keys():
                for _aid in self.device_scroll(**kwargs):
                    aids.update(_aid)

        if len(aids) > 0:
            self.logger.debug("Device details will be fetched for %d AIDs, in batches of %d." % (len(aids), batch_size))
        for aid_batch in self._chunker(list(aids), batch_size):
            try:
                r_params = {'ids': aid_batch}
                _resp = self.api_query(api_endpoint, r_params)
            except Exception as err:
                self.logger.error("Failed to %s.  %s" % (__name__, err))
                raise
            else:
                if _resp.success:
                    yield _resp.data
                else:
                    raise _resp.errors

    def device_containment(self, action_name, aids, api_endpoint='/devices/entities/devices-actions/v2'):
        """
        Contain or lift containment on a specified host. When contained, a host can only communicate with the
        CrowdStrike cloud and any IPs specified in your containment policy.
        :param action_name: [contain | lift_containment]
                            'contain' - This action contains the host, which stops any network communications to locations
                             other than the CrowdStrike cloud and IPs specified in your containment policy
                            'lift_containment': This action lifts containment on the host, which returns its network
                            communications to normal
        :param aids: The host agent ID (AID) of the host you want to contain. Provide the ID in JSON format with the key
                    ids and the value in square brackets, such as: "ids": ["123456789"]
        :param api_endpoint: see https://assets.falcon.crowdstrike.com/support/api/swagger.html#/
        :return: Three lists, list of successful, unsuccessful hosts and API errors.
        """
        if type(aids) is str:
            if aids.count(',') > 0:
                aids = aids.split(',')
            else:
                aids = [aids]

        r_params = {'action_name': action_name}
        r_data = {'ids': aids}

        # hostnames for friendly logging
        _hostnames = {}
        for hosts in self.device_details(aids):
            for host in hosts:
                _hostnames[host['device_id']] = host['hostname']

        self.logger.warning("Performing '%s' action on %s" % (action_name, ", ".join(_hostnames.values())))

        try:
            _resp = self.api_call(api_endpoint, params=r_params, payload=r_data)
        except Exception as err:
            self.logger.error("Failed to %s.  %s" % (__name__, err))
        else:
            _successful_hosts = []
            _failed_hosts = []
            if _resp.success:
                for data in _resp.data:
                    _successful_hosts.append(_hostnames[data['id']])
                if len(_successful_hosts) > 0:
                    self.logger.warning("Containment action '%s' successful on %s."
                                     % (action_name, ", ".join(_successful_hosts)))

                for error in _resp.errors:
                    _aid = aid_re.findall(error['message'])
                    if _aid:
                        _failed_hosts.append(_hostnames[_aid[0]])
                if len(_failed_hosts) > 0:
                    self.logger.error("Containment action '%s' failed on %s."
                                      % (action_name, ", ".join(_failed_hosts)))

            return _successful_hosts, _failed_hosts, _resp.errors

    def lift_containment(self, aids):
        """
        Remove containment from supplied list of AIDs.
        :param aids: list or AID CSV str.
        :return: Three lists, list of successful, unsuccessful hosts and API errors.
        """
        return self.device_containment('lift_containment', aids)

    def apply_containment(self, aids):
        """
        Place specified AIDs under containment.
        :param aids: list or AID CSV str.
        :return: Three lists, list of successful, unsuccessful hosts and API errors.
        """
        return self.device_containment('contain', aids)
