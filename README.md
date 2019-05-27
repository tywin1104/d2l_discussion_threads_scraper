# What this script is used for

With web automation, it will simulate web browser user and open up the desired course page in Avenue. It will then go on to the discussion page and check students' participation for the topics. It will check the next page should the results are not fully displayed in one page. Once the automation process is finished, the result json file will be generated and saved into the working directory.

## Warning before use

Due to the dynamic nature of website, the underlying HTML structure may change constantly. Should the current tool does not update to support the current version of D2L system, it could serve as a reference guide. With some modification( DOM elements, config...), it should behave as desired. The current codebase take example of a 2018 fall course and make all configuretions support this setup.

