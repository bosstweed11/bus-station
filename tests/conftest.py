#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def lockedBusStation(BusStation, accounts):
    etherInWei = 10 ** 18
    return BusStation.deploy(
        accounts[0], etherInWei, 4, 10 ** 20, {"from": accounts[1]}
    )


@pytest.fixture(scope="module")
def unlockedBusStation(BusStation, accounts, chain):
    etherInWei = 10 ** 18
    sleep_time = 5 * 60 * 60 * 24
    chain.sleep(sleep_time)
    return BusStation.deploy(
        accounts[0], etherInWei, 0, 10 ** 20, {"from": accounts[1]}
    )


@pytest.fixture(scope="module")
def discountBusStation(BusStation, accounts, chain):
    etherInWei = 10 ** 18
    sleep_time = 5 * 60 * 60 * 24
    chain.sleep(sleep_time)
    return BusStation.deploy(
        accounts[0], etherInWei, 0, 10 ** 10, {"from": accounts[1]}
    )


@pytest.fixture(scope="module")
def departedBus(BusStation, accounts, chain):
    etherInWei = 10 ** 18
    sleep_time = 5 * 60 * 60 * 24
    chain.sleep(sleep_time)
    deployed = BusStation.deploy(
        accounts[0], etherInWei, 0, 10 ** 20, {"from": accounts[1]}
    )

    # arrange
    riderOneAmount = 10 ** 18 - 1
    riderTwoAmount = 5
    startingDestinationBalance = accounts[0].balance()
    startingRiderOneBalance = accounts[1].balance()
    startingRiderTwoBalance = accounts[2].balance()

    # act
    deployed.buyBusTicket({"from": accounts[1], "amount": riderOneAmount})
    deployed.buyBusTicket({"from": accounts[2], "amount": riderTwoAmount})
    deployed.triggerBusRide()
    return deployed
