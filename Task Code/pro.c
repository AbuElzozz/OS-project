#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

void list_files(const char *path) {
    DIR *dir = opendir(path);
    struct dirent *entry;

    if (!dir) {
        perror("Unable to open directory");
        return;
    }

    printf("Listing files in directory: %s\n", path);
    while ((entry = readdir(dir)) != NULL) {
        printf("%s\n", entry->d_name);
    }
    closedir(dir);
}

// 777	anyone can do anything (read, write, or execute)
// 755	you can do anything; others can only read and execute
// 711	you can do anything; others can only execute
// 644	you can read and write; others can only read

void change_permissions(const char *path, const char *mode_str) {
    mode_t mode = strtol(mode_str, NULL, 8);
    if (chmod(path, mode) == -1) {
        perror("Failed to change permissions");
    } else {
        printf("Changed permissions of %s to %s\n", path, mode_str);
    }
}

void make_file(const char *path) {
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        perror("Failed to create file");
    } else {
        printf("File %s created\n", path);
        fclose(file);
    }
}

void delete_file(const char *path) {
    if (remove(path) == -1) {
        perror("Failed to delete file");
    } else {
        printf("File %s deleted\n", path);
    }
}

void make_directory(const char *path) {
    if (mkdir(path, 0755) == -1) {
        perror("Failed to create directory");
    } else {
        printf("Directory %s created\n", path);
    }
}

void delete_directory(const char *path) {
    if (rmdir(path) == -1) {
        perror("Failed to delete directory");
    } else {
        printf("Directory %s deleted\n", path);
    }
}

void create_symbolic_link(const char *target, const char *linkpath) {
    if (symlink(target, linkpath) == -1) {
        perror("Failed to create symbolic link");
    } else {
        printf("Symbolic link %s -> %s created\n", linkpath, target);
    }
}

int main() {
    char option;
    char path[256], target[256], mode[4];

    while (1) {
        printf("\nFile Manager Menu:\n");
        printf("A. List files/directories\n");
        printf("B. Change permissions of files\n");
        printf("C. Make/delete files/directories\n");
        printf("D. Create symbolic link files\n");
        printf("Q. Quit\n");
        printf("Enter your choice: ");
        scanf(" %c", &option);

        switch (option) {
            case 'A':
                printf("Enter path to list: ");
                scanf("%s", path);
                list_files(path);
                break;

            case 'B':
                printf("Enter path to change permissions: ");
                scanf("%s", path);
                printf("Enter mode (777,755,711,644): ");
                scanf("%s", mode);
                change_permissions(path, mode);
                break;

            case 'C':
                printf("Make or delete (m/d): ");
                char choice;
                scanf(" %c", &choice);
                if (choice == 'm') {
                    printf("File or directory (f/d): ");
                    char type;
                    scanf(" %c", &type);
                    printf("Enter path: ");
                    scanf("%s", path);
                    if (type == 'f') {
                        make_file(path);
                    } else if (type == 'd') {
                        make_directory(path);
                    } else {
                        printf("Invalid type\n");
                    }
                } else if (choice == 'd') {
                    printf("Enter path to delete: ");
                    scanf("%s", path);
                    struct stat st;
                    if (stat(path, &st) == 0 && S_ISDIR(st.st_mode)) {
                        delete_directory(path);
                    } else {
                        delete_file(path);
                    }
                } else {
                    printf("Invalid choice\n");
                }
                break;

            case 'D':
                printf("Enter target path: ");
                scanf("%s", target);
                printf("Enter symbolic link path: ");
                scanf("%s", path);
                create_symbolic_link(target, path);
                break;

            case 'Q':
                printf("Exiting...\n");
                return 0;

            default:
                printf("Invalid option. Try again.\n");
                break;
        }
    }

    return 0;
}

