/*!
    \file path.h
    \brief Filesystem path wrapper definition
    \author Ivan Shynkarenka
    \date 11.08.2016
    \copyright MIT License
*/

#ifndef CPPCOMMON_FILESYSTEM_PATH_H
#define CPPCOMMON_FILESYSTEM_PATH_H

#include "string/encoding.h"

#include <string>

namespace CppCommon {

//! Filesystem path
/*!
    Filesystem path wraps string directory, filename, symlink and other path types
    in a class and provide utility methods to check type of the path, status and
    permissions in a file system. Additionally path wrapper contains operators and
    methods for path manipulation (concatenation, canonization, absolute path).

    Path is managed in UTF-8 encoding!

    Not thread-safe.
*/
class Path
{
public:
    //! Default constructor
    Path() : _path() {}
    //! Initialize path with a given string value in UTF-8 encoding (Unix)
    /*!
        \param path - Path value in UTF-8 encoding
    */
    explicit Path(const std::string& path) : _path(path) {}
    //! Initialize path with a given string value in UTF-16 encoding (Windows)
    /*!
        \param path - Path value in UTF-16 encoding
    */
    explicit Path(const std::wstring& path) : _path(Encoding::ToUTF8(path)) {}
    Path(const Path&) = default;
    Path(Path&&) noexcept = default;
    ~Path() = default;

    Path& operator=(const std::string& path)
    { _path = path; return *this; }
    Path& operator=(const std::wstring& path)
    { _path = Encoding::ToUTF8(path); return *this; }
    Path& operator=(const Path&) = default;
    Path& operator=(Path&&) noexcept = default;

    // Append the given path with a path separator
    Path& operator/=(const std::string& path);
    Path& operator/=(const std::wstring& path)
    { return *this /= Path(path)._path; }
    Path& operator/=(const Path& path)
    { return *this /= path._path; }
    friend Path operator/(const Path& path1, const std::string& path2)
    { return Path(path1) /= path2; }
    friend Path operator/(const std::string& path1, const Path& path2)
    { return Path(path1) /= path2; }
    friend Path operator/(const Path& path1, const std::wstring& path2)
    { return Path(path1) /= path2; }
    friend Path operator/(const std::wstring& path1, const Path& path2)
    { return Path(path1) /= path2; }
    friend Path operator/(const Path& path1, const Path& path2)
    { return Path(path1) /= path2; }

    // Concatenate the given path without a path separator
    Path& operator+=(const std::string& path)
    { _path += path; return *this; }
    Path& operator+=(const std::wstring& path)
    { _path += Encoding::ToUTF8(path); return *this; }
    Path& operator+=(const Path& path)
    { _path += path._path; return *this; }
    friend Path operator+(const Path& path1, const std::string& path2)
    { return Path(path1) += path2; }
    friend Path operator+(const std::string& path1, const Path& path2)
    { return Path(path1) += path2; }
    friend Path operator+(const Path& path1, const std::wstring& path2)
    { return Path(path1) += path2; }
    friend Path operator+(const std::wstring& path1, const Path& path2)
    { return Path(path1) += path2; }
    friend Path operator+(const Path& path1, const Path& path2)
    { return Path(path1) += path2; }

    // Path comparison
    friend bool operator==(const Path& path1, const std::string& path2)
    { return path1._path == path2; }
    friend bool operator==(const std::string& path1, const Path& path2)
    { return path1 == path2._path; }
    friend bool operator==(const Path& path1, const std::wstring& path2)
    { return path1._path == Encoding::ToUTF8(path2); }
    friend bool operator==(const std::wstring& path1, const Path& path2)
    { return Encoding::ToUTF8(path1) == path2._path; }
    friend bool operator==(const Path& path1, const Path& path2)
    { return path1._path == path2._path; }
    friend bool operator!=(const Path& path1, const std::string& path2)
    { return path1._path != path2; }
    friend bool operator!=(const std::string& path1, const Path& path2)
    { return path1 != path2._path; }
    friend bool operator!=(const Path& path1, const std::wstring& path2)
    { return path1._path != Encoding::ToUTF8(path2); }
    friend bool operator!=(const std::wstring& path1, const Path& path2)
    { return Encoding::ToUTF8(path1) != path2._path; }
    friend bool operator!=(const Path& path1, const Path& path2)
    { return path1._path != path2._path; }
    friend bool operator<(const Path& path1, const std::string& path2)
    { return path1._path < path2; }
    friend bool operator<(const std::string& path1, const Path& path2)
    { return path1 < path2._path; }
    friend bool operator<(const Path& path1, const std::wstring& path2)
    { return path1._path < Encoding::ToUTF8(path2); }
    friend bool operator<(const std::wstring& path1, const Path& path2)
    { return Encoding::ToUTF8(path1) < path2._path; }
    friend bool operator<(const Path& path1, const Path& path2)
    { return path1._path < path2._path; }
    friend bool operator>(const Path& path1, const std::string& path2)
    { return path1._path > path2; }
    friend bool operator>(const std::string& path1, const Path& path2)
    { return path1 > path2._path; }
    friend bool operator>(const Path& path1, const std::wstring& path2)
    { return path1._path > Encoding::ToUTF8(path2); }
    friend bool operator>(const std::wstring& path1, const Path& path2)
    { return Encoding::ToUTF8(path1) > path2._path; }
    friend bool operator>(const Path& path1, const Path& path2)
    { return path1._path > path2._path; }
    friend bool operator<=(const Path& path1, const std::string& path2)
    { return path1._path <= path2; }
    friend bool operator<=(const std::string& path1, const Path& path2)
    { return path1 <= path2._path; }
    friend bool operator<=(const Path& path1, const std::wstring& path2)
    { return path1._path <= Encoding::ToUTF8(path2); }
    friend bool operator<=(const std::wstring& path1, const Path& path2)
    { return Encoding::ToUTF8(path1) <= path2._path; }
    friend bool operator<=(const Path& path1, const Path& path2)
    { return path1._path <= path2._path; }
    friend bool operator>=(const Path& path1, const std::string& path2)
    { return path1._path >= path2; }
    friend bool operator>=(const std::string& path1, const Path& path2)
    { return path1 >= path2._path; }
    friend bool operator>=(const Path& path1, const std::wstring& path2)
    { return path1._path >= Encoding::ToUTF8(path2); }
    friend bool operator>=(const std::wstring& path1, const Path& path2)
    { return Encoding::ToUTF8(path1) >= path2._path; }
    friend bool operator>=(const Path& path1, const Path& path2)
    { return path1._path >= path2._path; }

    //! Input instance from the given input stream
    friend std::istream& operator>>(std::istream& is, Path& instance)
    { is >> instance._path; return is; }
    //! Output instance into the given output stream
    friend std::ostream& operator<<(std::ostream& os, const Path& instance)
    { os << instance._path; return os; }

    //! Swap two instances
    friend void swap(Path& path1, Path& path2);

    //! Get the native path value
    const std::string& native() const noexcept { return _path; }

    //! Get the path value in UTF-8 format
    std::string string() const { return std::string(_path); }
    //! Get the path value in UTF-16 format
    std::wstring wstring() const { return Encoding::FromUTF8(_path); }

    //! Is the path empty?
    bool empty() const noexcept { return _path.empty(); }

    //! Clear path content
    void clear() noexcept { return _path.clear(); }

    //! Get the path separator character ('\' for Windows or '/' for Unix)
    static char separator();

protected:
    std::string _path;
};

/*! \example filesystem_path.cpp Filesystem path wrapper example */

} // namespace CppCommon

#include "path.inl"

#endif // CPPCOMMON_FILESYSTEM_PATH_H
