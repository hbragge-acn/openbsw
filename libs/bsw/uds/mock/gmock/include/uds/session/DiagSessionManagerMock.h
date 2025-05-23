// Copyright 2024 Accenture.

#pragma once

#include "uds/connection/IncomingDiagConnection.h"
#include "uds/session/IDiagSessionChangedListener.h"
#include "uds/session/IDiagSessionManager.h"

#include <gmock/gmock.h>

namespace uds
{
class DiagSessionManagerMock : public IDiagSessionManager
{
public:
    MOCK_CONST_METHOD0(getActiveSession, DiagSession const&());
    MOCK_METHOD0(startSessionTimeout, void());
    MOCK_METHOD0(stopSessionTimeout, void());
    MOCK_METHOD0(isSessionTimeoutActive, bool());
    MOCK_METHOD0(resetToDefaultSession, void());
    MOCK_METHOD0(persistAndRestoreSession, bool());

    MOCK_METHOD4(
        acceptedJob,
        DiagReturnCode::Type(
            IncomingDiagConnection&, AbstractDiagJob const&, uint8_t const[], uint16_t));
    MOCK_METHOD4(
        responseSent,
        void(IncomingDiagConnection&, DiagReturnCode::Type, uint8_t const[], uint16_t));

    MOCK_METHOD1(addDiagSessionListener, void(IDiagSessionChangedListener&));
    MOCK_METHOD1(removeDiagSessionListener, void(IDiagSessionChangedListener&));
};

} // namespace uds
