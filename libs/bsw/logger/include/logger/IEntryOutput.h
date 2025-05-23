// Copyright 2024 Accenture.

#pragma once

#include <estd/uncopyable.h>
#include <platform/estdint.h>

namespace util
{
namespace logger
{
class ComponentInfo;
class LevelInfo;
} // namespace logger

namespace format
{
class IPrintfArgumentReader;
}
} // namespace util

namespace logger
{
template<class E = uint32_t, class Timestamp = uint32_t>
class IEntryOutput : private ::estd::uncopyable
{
public:
    IEntryOutput();

    virtual void outputEntry(
        E entryIndex,
        Timestamp timestamp,
        ::util::logger::ComponentInfo const& componentInfo,
        ::util::logger::LevelInfo const& levelInfo,
        char const* str,
        ::util::format::IPrintfArgumentReader& argReader)
        = 0;
};

template<class E, class Timestamp>
inline IEntryOutput<E, Timestamp>::IEntryOutput() : ::estd::uncopyable()
{}

} // namespace logger
