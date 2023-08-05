from instaclient.client import *

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.client.checker import Checker


class Navigator(Checker):

    # NAVIGATION PROCEDURES
    def _nav_user(self:'InstaClient', user:str, check_user:bool=True):
        """
        Navigates to a users profile page

        Args:
            user:str: Username of the user to navigate to the profile page of
            check_user:bool: Condition whether to check if a user is valid or not

        Returns:
            True if operation is successful

        Raises:
            InvaildUserError if user does not exist
        """
        if check_user:
            result = self.is_valid_user(user=user)
        if self.driver.current_url != ClientUrls.NAV_USER.format(user):
            self.driver.get(ClientUrls.NAV_USER.format(user))

    
    def _nav_user_dm(self:'InstaClient', user:str, check_user:bool=True):
        """
        Open DM page with a specific user
        
        Args:
            user:str: Username of the user to send the dm to

        Raises:
            InvalidUserError if user does not exist

        Returns:
            True if operation was successful
        """
        try:
            self._nav_user(user, check_user=check_user)
            private = False
            LOGGER.debug('INSTACLIENT: User <{}> is valid and public (or followed)'.format(user))
        except PrivateAccountError:
            private = True
            LOGGER.debug('INSTACLIENT: User <{}> is private'.format(user))

        # TODO NEW VERSION: Opens DM page and creates new DM
        try:
            # LOAD PAGE
            LOGGER.debug('\n\nLOADING PAGE')
            self.driver.get(ClientUrls.NEW_DM)
            user_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USER_DIV)), wait_time=10)
            LOGGER.debug('Page Loaded')

            # INPUT USERNAME 
            input_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEARCH_USER_INPUT)), wait_time=15)
            LOGGER.debug(f'INPUT: {input_div}')
            input_div.send_keys(user)
            LOGGER.debug('Sent Username to Search Field')
            time.sleep(1)

            # FIND CORRECT USER DIV
            user_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USER_DIV)))
            username_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USER_DIV_USERNAME)))
            LOGGER.debug('Found user div')

            self._press_button(user_div)
            LOGGER.debug('Selected user div')
            time.sleep(1)
            next = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NEXT_BUTTON)))
            self._press_button(next)
            LOGGER.debug('Next pressed')
            return True
        except Exception as error:
            LOGGER.error('There was error navigating to the user page: ', exc_info=error)
            raise InstaClientError('There was an error when navigating to <{}>\'s DMs'.format(user))
            
    
    def _nav_post(self:'InstaClient', shortcode:str):
        url = ClientUrls.POST_URL.format(shortcode)
        if self.driver.current_url is not url:
            self.driver.get(url)

        result = self._is_valid_page(url)
        if not result:
            raise InvalidShortCodeError(shortcode)

        self._dismiss_useapp_bar()
        LOGGER.debug('Got Post\'s Page')
        return True


    def _nav_post_comments(self:'InstaClient', shortcode:str):
        url = ClientUrls.COMMENTS_URL.format(shortcode)
        if self.driver.current_url is not url:
            if self.driver.current_url == ClientUrls.POST_URL.format(shortcode):
                # Press Comment Button
                btn = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.COMMENT_BTN)))
                if btn:
                    btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.COMMENT_BTN)))
                    self._press_button(btn)
                else:
                    pass
            if self.driver.current_url != url:
                self.driver.get(url)

        result = self._is_valid_page(url)
        if not result:
            raise InvalidShortCodeError(shortcode)
        LOGGER.debug('Got Post\'s Comments Page')
        return True
        
     
    def _nav_tag(self:'InstaClient', tag:str):
        """
        Naviagtes to a search for posts with a specific tag on IG.

        Args:
            tag:str: Tag to search for
        """

        self.driver.get(ClientUrls.SEARCH_TAGS.format(tag))
        alert: WebElement = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)))
        if alert:
            # Tag does not exist
            raise InvaildTagError(tag=tag)
        else: 
            # Operation Successful
            return True
