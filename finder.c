#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <limits.h>

#ifdef _WIN32
    #include <windows.h>
    #define PATH_SEPARATOR '\\'
#else
    #include <unistd.h>
    #define PATH_SEPARATOR '/'
#endif

int num_dirs_searched = 0;
int num_files_searched = 0;

int search_item_recursive(const char* item_name, const char* directory) {
    DIR* dir;
    struct dirent* entry;
    struct stat statbuf;
    int found = 0;  // Flag to track if the item has been found

    dir = opendir(directory);
    if (dir == NULL) {
        perror("opendir");
        return found;
    }

    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, item_name) == 0) {
            char path[1024];
            snprintf(path, sizeof(path), "%s%c%s", directory, PATH_SEPARATOR, entry->d_name);
            printf("Path: %s\n", path);
            found = 1;  // Set the flag to 1 if the item is found
        }

        if (entry->d_type == DT_DIR && strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
            char path[1024];
            snprintf(path, sizeof(path), "%s%c%s", directory, PATH_SEPARATOR, entry->d_name);
            num_dirs_searched++;
            found |= search_item_recursive(item_name, path);
        }
        else {
            num_files_searched++;
        }
    }

    closedir(dir);

    return found;
}

void find_item_recursive(const char* item_name, const char* starting_directory) {
    struct stat statbuf;
    if (stat(starting_directory, &statbuf) != 0) {
        perror("stat");
        return;
    }

    if (!S_ISDIR(statbuf.st_mode)) {
        printf("Invalid starting directory.\n");
        return;
    }

    int found = search_item_recursive(item_name, starting_directory);

    if (!found)
        printf("Item not found\n");
}

char* get_current_directory() {
#ifdef _WIN32
    DWORD buffer_size = GetCurrentDirectory(0, NULL);
    char* current_directory = malloc(buffer_size);
    GetCurrentDirectory(buffer_size, current_directory);
    return current_directory;
#else
    char* current_directory = malloc(PATH_MAX);
    getcwd(current_directory, PATH_MAX);
    return current_directory;
#endif
}

int main(int argc, char* argv[]) {
    if (argc != 3 && argc != 4) {
        printf("Invalid number of arguments.\n");
        printf("Usage: ./program -file filename.ext OR ./program -folder foldername [starting_directory]\n");
        return 1;
    }

    char* option = argv[1];
    char* item_name = argv[2];
    char* starting_directory;

    if (argc == 4) {
        starting_directory = argv[3];
    } else {
        starting_directory = get_current_directory();
    }

    if (strcmp(option, "-file") == 0) {
        find_item_recursive(item_name, starting_directory);
    }
    else if (strcmp(option, "-folder") == 0) {
        find_item_recursive(item_name, starting_directory);
    }
    else {
        printf("Invalid option.\n");
        printf("Usage: ./program -file filename.ext OR ./program -folder foldername [starting_directory]\n");
        return 1;
    }

    printf("\nTotal directories searched: %d\n", num_dirs_searched);
    printf("Total files searched: %d\n", num_files_searched);

    // Free memory if current_directory is dynamically allocated
    if (argc != 4) {
        free(starting_directory);
    }

    return 0;
}
