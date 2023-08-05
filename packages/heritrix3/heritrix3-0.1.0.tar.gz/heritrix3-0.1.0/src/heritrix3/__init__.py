__version__ = "0.1.0"

import os
import time

import requests
from lxml import etree
from requests.auth import HTTPDigestAuth

# ---------------------------------------------------------------------------

__all__ = ["HeritrixAPIError", "HeritrixAPI"]

# ---------------------------------------------------------------------------


def disable_ssl_warnings():
    """Quieten SSL insecure warnings.

    See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
    """
    import urllib3

    urllib3.disable_warnings()


# ---------------------------------------------------------------------------


class HeritrixAPIError(Exception):
    def __init__(self, message: str, *args, **kwargs):
        self.message = message
        self.response = kwargs.pop("response", None)
        super(HeritrixAPIError, self).__init__(message, *args, **kwargs)

    def __str__(self):
        return f"HeritrixAPIError: {self.message}"


# ---------------------------------------------------------------------------


class HeritrixAPI:
    def __init__(
        self,
        host: str = "https://localhost:8443/engine",
        user: str = "admin",
        passwd: str = "",
        verbose: bool = False,
        insecure: bool = True,
        headers=None,
        timeout=None,
    ):
        self.host = host
        self.auth = HTTPDigestAuth(user, passwd)
        self.verbose = verbose
        self.insecure = insecure
        self.timeout = timeout

        # strip trailing slashes
        if self.host:
            self.host = self.host.rstrip("/")

        self.headers = {"Accept": "application/xml"}

        if isinstance(headers, dict):
            self.headers.update(headers)

        self.last_response = None

    def _post(
        self, url=None, data=None, headers=None, code=None, timeout=None, raw=True
    ):
        if not url:
            url = self.host

        headers_copy = dict(self.headers)
        if headers is not None:
            headers_copy.update(headers)

        if data is None:
            data = dict()

        resp = requests.post(
            url,
            auth=self.auth,
            data=data,
            headers=headers_copy,
            verify=not self.insecure,
            timeout=self.timeout if timeout is None else timeout,
        )
        self.last_response = resp

        if code is not None and resp.status_code != code:
            raise HeritrixAPIError(
                f"Invalid response code: expected: {code}, got: {resp.status_code}, url={url}"
            )

        if not raw:
            resp = self._xml2json(resp.text)

        return resp

    def _get(
        self,
        url=None,
        headers=None,
        api_headers=True,
        code=None,
        timeout=None,
        raw=True,
    ):
        if not url:
            url = self.host

        headers_copy = dict()
        if api_headers:
            headers_copy.update(self.headers)
        if headers is not None:
            headers_copy.update(headers)

        resp = requests.get(
            url,
            auth=self.auth,
            headers=headers_copy,
            verify=not self.insecure,
            timeout=self.timeout if timeout is None else timeout,
        )
        self.last_response = resp

        if code is not None and resp.status_code != code:
            raise HeritrixAPIError(
                f"Invalid response code: expected: {code}, got: {resp.status_code}; url={url}"
            )

        if not raw:
            resp = self._xml2json(resp.text)

        return resp

    def _post_action(
        self, action: str, url=None, data=None, headers=None, code=None, raw=True
    ):
        if not action:
            raise ValueError("Missing action.")

        if data is None:
            data = dict()

        data["action"] = action

        return self._post(url=url, data=data, headers=headers, code=code, raw=raw)

    def _job_action(self, action: str, job_name: str, data=None, code=None, raw=True):
        if not job_name:
            raise ValueError("Missing job name.")

        url = f"{self.host}/job/{job_name}"

        return self._post_action(action, url, data=data, code=code, raw=raw)

    # --------------------------------

    def info(self, job_name: str = None, raw: bool = False):
        url = None
        if job_name is not None:
            url = f"{self.host}/job/{job_name}"

        resp = self._get(url=url, code=200, raw=raw)

        return resp

    def get_job_actions(self, job_name: str):
        # info = self.info(job_name=job_name, raw=False)
        # return info["job"]["availableActions"]["value"]
        resp = self.info(job_name=job_name, raw=True)
        xml_doc = etree.fromstring(resp.text)
        actions = xml_doc.xpath("/job/availableActions/value/text()")
        return actions

    def wait_for_action(self, job_name: str, action: str, timeout=20, poll_delay=1):
        if poll_delay <= 0:
            raise ValueError("poll_delay mustn't be negative or null!")

        time_start = time.time()

        avail_actions = self.get_job_actions(job_name)
        while action not in avail_actions:
            if timeout is not None and (time.time() - time_start > timeout):
                # raise TimeoutError
                return False

            time.sleep(poll_delay)
            avail_actions = self.get_job_actions(job_name)

        return True

    # --------------------------------

    def create(self, job_name: str, raw: bool = False):
        if not job_name:
            raise ValueError("Missing job name.")

        return self._post_action("create", data={"createpath": job_name}, raw=raw)

    def add(self, job_dir: str, raw: bool = False):
        if not job_dir:
            raise ValueError("Missing job directory.")
        # TODO: check that a cxml file is in the directory?

        return self._post_action("add", data={"addpath": job_dir}, raw=raw)

    # --------------------------------

    def build(self, job_name: str, raw: bool = False):
        return self._job_action("build", job_name, raw=raw)

    def launch(self, job_name: str, checkpoint=None, raw: bool = False):
        data = None
        if checkpoint is not None:
            data = {"checkpoint": checkpoint}

        return self._job_action("launch", job_name, data=data, raw=raw)

    def pause(self, job_name: str, raw: bool = False):
        return self._job_action("pause", job_name, raw=raw)

    def unpause(self, job_name: str, raw: bool = False):
        return self._job_action("unpause", job_name, raw=raw)

    def terminate(self, job_name: str, raw: bool = False):
        return self._job_action("terminate", job_name, raw=raw)

    def teardown(self, job_name: str, raw: bool = False):
        return self._job_action("teardown", job_name, raw=raw)

    def checkpoint(self, job_name: str, raw: bool = False):
        return self._job_action("checkpoint", job_name, raw=raw)

    # --------------------------------

    def rescan(self, raw=False):
        return self._post_action("rescan", raw=raw)

    def copy(
        self,
        job_name: str,
        new_job_name: str,
        as_profile: bool = False,
        raw: bool = False,
    ):
        if not new_job_name:
            raise ValueError("new_job_name must not be empty!")

        data = dict()
        data["copyTo"] = new_job_name
        if as_profile:
            data["as_profile"] = "on"

        return self._job_action("copy", job_name, data=data, raw=raw)

    # --------------------------------

    def execute_script(
        self, job_name: str, script: str, engine: str = "beanshell", raw: bool = False
    ):
        if not job_name:
            raise ValueError("Missing job name.")
        if not script:
            raise ValueError("Missing script?")
        if engine not in ("beanshell", "js", "groovy", "AppleScriptEngine"):
            raise ValueError(f"Invalid script engine param: {engine}")

        data = dict()
        data["engine"] = engine
        data["script"] = script

        url = f"{self.host}/job/{job_name}/script"

        return self._post(url=url, data=data, raw=raw)

    # --------------------------------

    def send_file(self, job_name: str, filepath, name=None):
        if not job_name:
            raise ValueError("Missing job name.")
        if not filepath:
            raise ValueError("Missing filepath.")
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            raise HeritrixAPIError(f"File does not exist!, {filepath}")

        if not name:
            name = os.path.basename(filepath)
        url = f"{self.host}/job/{job_name}/jobdir/{name}"
        # TODO: check config url with :func:`get_config_url()` ?

        with open(filepath, "rb") as fdat:
            resp = requests.put(
                url,
                auth=self.auth,
                data=fdat,
                headers=self.headers,
                verify=not self.insecure,
            )
        return resp.ok

    def send_config(self, job_name: str, cxml_filepath):
        if not job_name:
            raise ValueError("Missing job name.")
        if cxml_filepath is None or cxml_filepath == "":
            raise ValueError("Missing cxml filepath name.")
        if not os.path.exists(cxml_filepath) or not os.path.isfile(cxml_filepath):
            raise HeritrixAPIError(f"CXML file does not exist!, {cxml_filepath}")

        return self.send_file(job_name, cxml_filepath, "crawler-beans.cxml")

    def get_config_url(self, job_name: str):
        if not job_name:
            raise ValueError("Missing job name.")

        resp = self.info(job_name=job_name, raw=True)
        if not resp:
            raise HeritrixAPIError(
                f"Error retrieving job info! {resp.status_code}"
                f" - {resp.reason}, url={resp.url}"
            )

        xml_doc = etree.fromstring(resp.text)
        config_url = xml_doc.xpath("/job/primaryConfigUrl[1]/text()")
        if not config_url:
            raise HeritrixAPIError("Invalid job configuration document?")

        return config_url[0]

    def get_config(self, job_name: str, raw: bool = True):
        config_url = self.get_config_url(job_name)

        resp = self._get(url=config_url, code=200, raw=raw)

        return resp.text

    # --------------------------------
    # --------------------------------

    @classmethod
    def _xml2json(cls, xml_str):
        if isinstance(xml_str, str):
            xml_doc = etree.fromstring(xml_str)
        elif isinstance(xml_str, etree._Element):
            xml_doc = xml_str
        else:
            raise TypeError(f"Invalid xml_str type, got: {type(xml_str)}")

        return cls.__tree_to_dict(xml_doc)

    @classmethod
    def __tree_to_dict(cls, tree):
        # see: https://github.com/WilliamMayor/hapy/blob/master/hapy/hapy.py#L213
        if len(tree) == 0:
            return {tree.tag: tree.text}
        D = {}
        for child in tree:
            d = cls.__tree_to_dict(child)
            tag = list(d.keys())[0]
            try:
                try:
                    D[tag].append(d[tag])
                except AttributeError:
                    D[tag] = [D[tag], d[tag]]
            except KeyError:
                D[tag] = d[tag]
        return {tree.tag: D}

    # --------------------------------

    def list_jobs(self, status=None, unbuilt: bool = False):
        resp = self._get(raw=True)
        xml_doc = etree.fromstring(resp.text)

        if unbuilt:
            # if unbuilt, then search for those only
            jobs = xml_doc.xpath("//jobs/value[./statusDescription = 'Unbuilt']")
        elif status is not None:
            # then search for crawlControllerState
            jobs = xml_doc.xpath(f"//jobs/value[./crawlControllerState = '{status}']")
        else:
            # else all
            jobs = xml_doc.xpath("//jobs/value")

        job_names = [job.find("shortName").text for job in jobs]
        return job_names

    def get_launchid(self, job_name: str):
        script = "rawOut.println( appCtx.getCurrentLaunchId() );"
        resp = self.execute_script(
            job_name, script=script, engine="beanshell", raw=True
        )
        if not resp.ok:
            if resp.status_code == 500:
                # most probably not application context / unbuilt job
                return None

            raise HeritrixAPIError(
                f"No launchid found: {resp.status_code} - {resp.reason}"
            )

        tree = etree.fromstring(resp.text)
        ret = tree.find("rawOutput").text.strip()
        if ret == "null":
            # build but not launched?
            return None
        return ret

    def crawl_report(self, job_name: str, launch_id=None):
        if launch_id is None:
            try:
                # if no launchid - try to get with "latest"
                url = (
                    f"{self.host}/job/{job_name}/jobdir/latest/reports/crawl-report.txt"
                )

                resp = self._get(url=url, api_headers=False, raw=True)
                return resp.text
            except Exception as ex:
                # if that fails, try to query the launch_id and try again
                launch_id = self.get_launchid(job_name)

                if launch_id is None:
                    # unbuilt job?
                    # either it got anything with latest or there simply was not yet a crawl
                    raise HeritrixAPIError(
                        f"Unbuilt Job {job_name}, check if has ever crawled?"
                    ) from ex

                return self.crawl_report(job_name, launch_id=launch_id)

        # ----------------------------

        url = f"{self.host}/job/{job_name}/jobdir/{launch_id}/reports/crawl-report.txt"

        resp = self._get(url=url, api_headers=False, raw=True)
        return resp.text

    # --------------------------------

    def list_files(
        self, job_name: str, gather_files: bool = True, gather_folders: bool = True
    ):
        script_fileout = """
            it.eachFile {
                rawOut.println( it );
            };
        """.strip()
        if not gather_files:
            script_fileout = ""

        script_folder_out = """
            rawOut.println( it )
        """.strip()
        if not gather_folders:
            script_folder_out = ""

        script = f"""
        def listRecurs;
        listRecurs = {{
            it.eachDir( listRecurs );
            {script_fileout}
            {script_folder_out}
        }};
        listRecurs( job.jobDir )
        """

        resp = self.execute_script(job_name, script=script, engine="groovy", raw=True)

        if not resp.ok:
            if resp.status_code == 500:
                # most probably not application context / unbuilt job
                return []

            raise HeritrixAPIError(
                f"Error executing listRecurs script: {resp.status_code} - {resp.reason}"
            )

        tree = etree.fromstring(resp.text)
        outtree = tree.find("rawOutput")
        if outtree is None:
            error = "No error output found?!"
            errtree = tree.find("exception")
            if errtree is not None:
                error = errtree.text
            raise HeritrixAPIError(f"Error executing listRecurs script: {error}")

        text = outtree.text.strip()
        lines = [ln.strip() for ln in text.splitlines()]
        return lines

    def list_warcs(self, job_name: str, launchid=None):
        if not launchid:
            launchid = "latest"

        script = f"""
        warcDir = new File( job.jobDir, "{launchid}/warcs" )
        warcDir.eachFile {{
            rawOut.println( it );
        }};
        """.strip()

        resp = self.execute_script(job_name, script=script, engine="groovy", raw=True)

        if not resp.ok:
            if resp.status_code == 500:
                # most probably not application context / unbuilt job
                return []

            raise HeritrixAPIError(
                f"Error executing list_warcs script: {resp.status_code} - {resp.reason}"
            )

        tree = etree.fromstring(resp.text)
        outtree = tree.find("rawOutput")
        if outtree is None:
            error = "No error output found?!"
            errtree = tree.find("exception")
            if errtree is not None:
                error = errtree.text
            raise HeritrixAPIError(f"Error executing list_warcs script: {error}")

        text = outtree.text.strip()
        lines = [ln.strip() for ln in text.splitlines()]
        return lines

    def delete_job_dir(self, job_name: str):
        script = """
        def delRecurs;
        delRecurs = {
            it.eachDir( delRecurs );
            it.eachFile {
                it.delete();
            };
            it.delete();
        };
        delRecurs( job.jobDir )
        """

        resp = self.execute_script(job_name, script=script, engine="groovy", raw=True)

        if not resp.ok:
            raise HeritrixAPIError(
                f"Error executing delRecurs script: {resp.status_code} - {resp.reason}"
            )

    # --------------------------------


# ---------------------------------------------------------------------------
