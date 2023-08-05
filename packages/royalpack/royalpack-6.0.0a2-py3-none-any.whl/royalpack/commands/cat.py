# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
import aiohttp
import royalnet.engineer as engi
import logging
import io

# Internal imports
# from . import something

# Special global objects
log = logging.getLogger(__name__)


# Code
@engi.PartialCommand.new(syntax="")
async def cat(*, _sentry: engi.Sentry, _msg: engi.Message, **__):
    """
    Send a cat in the chat! 🐈
    """

    log.debug("Creating a new HTTP session")
    async with aiohttp.ClientSession() as session:

        log.info("Making a GET request to The Cat API Image Search")
        async with session.get("https://api.thecatapi.com/v1/images/search") as response:

            log.debug("Ensuring the request was successful")
            if response.status >= 400:
                log.error(f"The Cat API returned an HTTP error: {response.status}")
                await _msg.send_reply(
                    text="⚠️ Couldn't request a cat from https://thecatapi.com :("
                )
                return

            log.debug("Reading the JSON received from The Cat API")
            try:
                result = await response.json()
            except aiohttp.ContentTypeError:
                log.error(f"Couldn't decode received JSON from The Cat API")
                await _msg.send_reply(
                    text="⚠️ Couldn't understand what the cat from https://thecatapi.com was saying :("
                )
                return

        # Example result:
        # [
        #     {
        #         "breeds": [],
        #         "id": "MjAzMjY3MQ",
        #         "url": "https://cdn2.thecatapi.com/images/MjAzMjY3MQ.jpg",
        #         "width": 557,
        #         "height": 724
        #     }
        # ]

        log.debug("Ensuring at least one image was received")
        if len(result) == 0:
            log.error("Didn't receive any image from The Cat API")
            await _msg.send_reply(
                text="⚠️ I couldn't find any cats at https://thecatapi.com :("
            )
            return

        # Select the first image received
        selected_cat = result[0]
        log.debug(f"Selected {selected_cat!r}")

        log.debug("Ensuring an image url is available")
        if "url" not in selected_cat:
            log.error("Image received from The Cat API did not have any URL")
            await _msg.send_reply(
                text="⚠️ I found a cat at https://thecatapi.com, but I couldn't find its image :("
            )
            return

        # Download the cat image
        log.info("Making a GET request to retrieve a The Cat API image")
        async with session.get(selected_cat["url"]) as response:

            log.debug("Reading image bytes into memory")
            img = io.BytesIO()
            while img_data := response.content.read(8192):
                img.write(img_data)

    log.debug("Sending image in the chat")
    await _msg.send_reply(files=[img])


# Objects exported by this module
__all__ = (
    "cat",
)
