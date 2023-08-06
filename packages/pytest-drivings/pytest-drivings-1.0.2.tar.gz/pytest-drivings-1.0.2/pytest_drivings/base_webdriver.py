import time
from deprecation import deprecated
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumRemoteWebDriver
from dill.source import getsource
from pytest_drivings.exceptions import TabNotOpenException
from seleniumrequests.request import RequestMixin


class BaseWebDriver(SeleniumRemoteWebDriver, RequestMixin):
    def open_blank_tab(self):
        """
        Open a blank tab in the background, stay on the current tab.
        Keeps the webdriver focused on the tab that was focused previously.
        :return: the window handle of the tab that was just opened
        """
        prev_handles = set(self.window_handles)
        prev_handle = self.current_window_handle
        new_tab_script = f"window.open('about:blank', 'new_tab_{len(prev_handles)}')"
        self.execute_script(new_tab_script)
        current_handles = set(self.window_handles)
        new_handles = current_handles.difference(prev_handles)
        if len(new_handles) < 1:
            raise TabNotOpenException(
                "open_blank_tab did not open a blank tab "
                "after executing the following JavaScript:\n"
                f"{new_tab_script}"
            )
        self.switch_to.window(prev_handle)
        return new_handles[0]

    def load_page_in_tab(self, window_handle, page_class, *page_args, **page_kwargs):
        """
        Creates an instance of the given page class in the tab represented by the given window handle.
        Keeps the webdriver focused on the tab that was focused previously.

        Passing a webdriver into this function for page construction is OPTIONAL.
        If no webdriver is supplied, this instance will be injected into the constructor.

        :param window_handle: unique ID for the tab you wish to load a new page in.
        :param page_class: the class of the page you want to instantiate
        :param page_args: positional arguments to the page constructor
        :param page_kwargs: keyword arguments to the page constructor
        :return: ( newly constructed instance of your page, window handle of the new tab )

        Example Usage:
            - Load an instance of the LoginPage in a given window, switch to the new handle:
                new_page, handle = webdriver.load_page_in_tab(handle, LoginPage, next_page=HomePage, pre_loaded=False)
                webdriver.switch_to.window(handle)
        """
        prev_handle = self.current_window_handle
        self.switch_to.window(window_handle)
        # decide if we need to supply a webdriver, or if one is supplied
        need_wd = any(
            [
                isinstance(arg, BaseWebDriver)
                for arg in page_args + tuple(page_kwargs.values())
            ]
        )
        # return an instance of the page
        page_instance = (
            page_class(self, *page_args, **page_kwargs)
            if need_wd
            else page_class(*page_args, **page_kwargs)
        )
        self.switch_to.window(prev_handle)
        return page_instance, window_handle

    def load_page_in_new_tab(self, page_class, *page_args, **page_kwargs):
        """
        Creates an instance of the given page class in a NEW tab.
        Keeps the webdriver focused on the tab that was focused previously.

        Passing a webdriver into this function for page construction is OPTIONAL.
        If no webdriver is supplied, this instance will be injected into the constructor.

        :param page_class: the class of the page you want to instantiate
        :param page_args: positional arguments to the page constructor
        :param page_kwargs: keyword arguments to the page constructor
        :return: ( newly constructed instance of your page, window handle of the new tab )

        Example usage:
            - Open a new tab and force the webdriver to load a new instance of the LoginPage with custom kwargs:
                new_page, new_window = webdriver.load_page_in_new_tab(LoginPage, next_page=HomePage, pre_loaded=False)
                webdriver.switch_to.window(new_window)
        """
        new_handle = self.open_blank_tab()
        return self.load_page_in_tab(new_handle, page_class, *page_args, **page_kwargs)

    def open_new_tab_via_action(self, action, *action_args, **action_kwargs):
        """
        Execute a given action.
        Assert that the action opened a new tab.
        Direct the webdriver to focus on the new tab.

        :param action: the action to be executed
        :param action_args: positional arguments for the action
        :param action_kwargs: keyword arguments for the action
        :return: ( return value of the supplied action, window handle of the newly opened tab )

        Example usage:
            - Open new tab via button press, create an instance of the page that you opened:
                webdriver.open_new_tab_via_action(lambda: my_button.click(webdriver))
                new_page = MyPage(webdriver, pre_loaded=True)

            - Open new tab via function call, passing in args and kwargs:
                return_value, new_handle = webdriver.open_new_tab_via_action(my_function, arg1, arg2,
                                                                             kwarg1=val1, kwarg2=val2)
                new_page = MyPage(web_driver, pre_loaded=True)
        """
        prev_handles = set(self.window_handles)
        action_ret_val = action(*action_args, **action_kwargs)
        current_handles = set(self.window_handles)
        new_handles = current_handles.difference(prev_handles)
        if len(new_handles) < 1:
            raise TabNotOpenException(
                f"The action provided to open_new_tab_via_action did not open a new tab. \n"
                f"{self._get_action_debug_string(action, *action_args, **action_kwargs)}"
            )
        self.switch_to.window(list(new_handles)[0])
        return action_ret_val, list(new_handles)[0]

    @staticmethod
    def _get_action_debug_string(action, *action_args, **action_kwargs):
        result = f"Action: \n {getsource(action)}\n"
        if len(action_args) > 0:
            result += f"Provided args: {action_args} \n"
        if len(action_kwargs) > 0:
            result += f"Provided kwargs: {action_kwargs} \n"
        return result

    @deprecated(
        deprecated_in="1.0.1",
        details="Use `load_page_in_tab/load_page_in_new_tab` instead.",
    )
    def wait_for_new_tab_to_open(self, timeout=10):
        tries = 0
        while len(self.window_handles) == 1:
            if tries > timeout:
                raise TimeoutError("Timeout waiting for the new tab to open")
            time.sleep(1)
            tries += 1

    @deprecated(
        deprecated_in="1.0.1",
        details="Use `load_page_in_tab/load_page_in_new_tab` instead.",
    )
    def wait_for_tab_to_load(self, page, timeout=10):
        tries = 0
        while "about:blank" in self.current_url:
            if tries > timeout:
                raise TimeoutError("Timeout waiting for the tab to load.")
            time.sleep(1)
            tries += 1

    @deprecated(
        deprecated_in="1.0.1", details="Use webdriver.switch_to.window(window_handle)"
    )
    def switch_to_tab(self, handle_index: int):
        self.switch_to.window(self.window_handles[handle_index])

    @deprecated(
        deprecated_in="1.0.1",
        details="Use webdriver.current_window_handle "
        "to get a unique string that identifies your current window",
    )
    def get_current_tab_index(self):
        """
        Function for getting the index of the current tab
        """
        current_handle = self.current_window_handle
        all_handles = self.window_handles
        return all_handles.index(current_handle)

    @deprecated(
        deprecated_in="1.0.1",
        details="Use: webdriver.switch_to.window(window_handle) and then webdriver.close()",
    )
    def close_tab(self, handle_index: int):
        self.switch_to.window(self.window_handles[handle_index])
        self.close()
        if len(self.window_handles) > 0:
            self.switch_to.window(self.window_handles[0])
