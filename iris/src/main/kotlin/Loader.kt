package org.fpeterek.mad.iris

import java.io.File
import java.util.stream.Collectors


object Loader {

    private fun <T> parseLine(line: String, parser: (List<String>) -> T) = line
        .replace(',', '.')
        .split(";")
        .let {
            parser(it)
        }

    fun <T> loadFile(filename: String, parser: (List<String>) -> T): MutableList<T> = File(filename)
        .inputStream()
        .bufferedReader()
        .lines()
        .skip(1)
        .filter { it.isNotBlank() }
        .map { parseLine(it, parser) }
        .collect(Collectors.toList())
}
