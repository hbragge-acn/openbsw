// Copyright 2024 Accenture.

#pragma once

#include "bsp/power/IEcuPowerStateController.h"

#include <gmock/gmock.h>

using namespace ::bios;

namespace power
{
class EcuPowerStateControllerMock : public IEcuPowerStateController
{
public:
    MOCK_METHOD0(startPreSleep, void());
    MOCK_METHOD2(powerDown, uint32_t(uint8_t mode, tCheckWakeupDelegate delegate));
    MOCK_METHOD1(powerDown, uint32_t(uint8_t mode));
    MOCK_METHOD0(fullPowerUp, void());
    MOCK_METHOD3(setWakeupSourceMonitoring, void(uint32_t source, bool active, bool fallingEdge));
    MOCK_METHOD1(clearWakeupSourceMonitoring, void(uint32_t source));
    MOCK_METHOD1(setWakeupDelegate, bool(tCheckWakeupDelegate& delegate));
    MOCK_METHOD0(getWakeupSource, uint32_t(void));
};

} // namespace power
