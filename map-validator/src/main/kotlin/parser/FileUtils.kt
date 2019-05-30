package parser

import java.io.File
import java.io.IOException
import java.util.stream.Collectors

class FileUtils {
    companion object {
        @JvmStatic
        fun readFile(path: String): String {
            val file = File(path)

            if (!file.exists()) {
                throw IOException("File does not exist: $path")
            }

            return file.readLines().stream()
                    .map { it.trim() }
                    .collect(Collectors.toList())
                    .joinToString(separator = "")
        }
    }
}