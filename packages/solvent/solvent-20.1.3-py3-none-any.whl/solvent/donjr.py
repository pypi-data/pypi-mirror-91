import log
import pomace
import random


def main():
    submits = 0
    errors = 0

    pomace.freeze()

    while errors < 10:
        person = pomace.fake.person
        slug = random.choice(
            [
                "liberal-privilege-joe-biden-and-the-democrat-s-defense-of-the-indefensible",
                "liberal-privilege-joe-biden-and-the-democrat-s-defense-of-the-indefensible-signed-copy",
                "liberal-privilege-triggered-book-bundle",
                "triggered",
                "aoc-special-liberal-privilege-joe-biden-and-the-democrats-defense-of-the-indefensible-signed-copy",
            ]
        )

        page = pomace.visit("http://donjr.com")

        log.info(f"Beginning iteration as {person.first_name}")
        page.fill_email_address(person.email_address)
        page = page.click_submit()

        if "Not Found" in page:
            log.warn(f"Handling 404 page: {page.url}")
            page = page.click_continue_shopping()
            page = page.click_shop_now()
        elif "let us know you're not a robot" in page:
            log.warn(f"Skipping CAPCHA: {page.url}")
            page = pomace.visit(f"https://donjr.com/collections/all/products/{slug}")
        else:
            log.info("Closing confirmaiton and going to store")
            page = page.click_close()
            page = page.click_shop_now()

        log.info("Adding book to cart")
        page = page.click_buy_it_now(delay=2, wait=5)

        if "Contact information" not in page:
            log.info("Resetting checkout form")
            page = page.click_change()

        log.info("Checking out")
        page.fill_email(person.email)
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_address(person.address)
        page.type_enter()
        page = page.click_continue_to_shipping()

        if "Shipping method" not in page:
            errors += 1
            log.error(f"Address submission failed (errors: {errors})")
            continue

        log.info("Continuing to payment")
        page = page.click_continue_to_payment()

        log.info("Completing order")
        page.click_paypal()
        page = page.click_complete_order()

        if "paypal" in page.url:
            submits += 1
            errors = 0
            log.info(f"Completed iterations: {submits}")
        else:
            errors += 1
            log.error(f"Order submission failed (errors: {errors})")
