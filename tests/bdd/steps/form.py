from behave import when

from selenium.webdriver.common.by import By


@when('I fill out the form')
def do_form_fill_out(context):
    for row in context.table:
        field = context.browser.find_element(by=By.ID, value=row['field'])
        value = row['value']
        if value == "on" or value == "off":
            if value == "on" and not field.is_selected() or value == "off" and field.is_selected():
                field.click()
        else:
            field.send_keys(row['value'])
    button = context.browser.find_elements(by=By.CSS_SELECTOR, value='input[type=submit]')[-1]
    button.click()
