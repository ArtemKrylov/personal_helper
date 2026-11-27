COMMAND_HELP = {
    # General commands
    "hello": (
        "hello",
        "hello",
        "Greets the user and offers assistance.",
    ),
    "help": (
        "help [command] [desc]",
        "help add-birthday desc",
        "Displays all available commands. Specify a command "
        "to see its usage and example, or add 'desc' "
        "to view its detailed description.",
    ),
    "commands": (
        "commands",
        "commands",
        "Displays all available commands list in short.",
    ),
    # Contact management
    "add": (
        "add <name> <phone> [birthday]",
        "add Peter 1234567890 14.06.2002",
        "Creates a new contact with a name, phone number "
        "and an optional birthday. If the contact already "
        "exists, asks for confirmation before updating it.",
    ),
    "change": (
        "change <name> <phone> [birthday]",
        "change Peter 0987654321",
        "Updates an existing contact. Replaces its current "
        "phone numbers with the provided phone number and "
        "updates the birthday if specified.",
    ),
    "del": (
        "del <name>",
        "del Peter",
        "Permanently removes a contact and all its associated "
        "information from the address book.",
    ),
    "show": (
        "show <name>",
        "show Peter",
        "Displays detailed information about a specific " "contact in a table format.",
    ),
    "all": (
        "all",
        "all",
        "Displays all saved contacts and their associated "
        "information in a table format.",
    ),
    # Phone management
    "add-phone": (
        "add-phone <name> <phone>",
        "add-phone Peter 0987654321",
        "Adds an additional phone number to a contact. "
        "Duplicate phone numbers are not allowed. "
        "If the contact does not exist, offers to create it.",
    ),
    "change-phone": (
        "change-phone <name> <old-phone> <new-phone>",
        "change-phone Peter 0987654321",
        "Changes contact phone number from old-phone to new-phone"
        "If phone already exists - prints it",
    ),
    "del-phone": (
        "del-phone <name> <phone>",
        "del-phone Peter 0987654321",
        "Deletes entered phone number from contacts phones"
        "If the phone number does not exist, prints it.",
    ),
    "phones": (
        "phones <name>",
        "phones Peter",
        "Displays all phone numbers associated with " "the specified contact.",
    ),
    # Birthday management
    "add-birthday": (
        "add-birthday <name> <birthday>",
        "add-birthday Peter 14.06.2002",
        "Assigns a birthday to an existing contact. "
        "The date must be in DD.MM.YYYY format. "
        "If a birthday already exists, asks for confirmation "
        "before replacing it.",
    ),
    "show-birthday": (
        "show-birthday <name>",
        "show-birthday Peter",
        "Displays the birthday of the specified contact.",
    ),
    "change-birthday": (
        "change-birthday <name> <birthday>",
        "change-birthday Peter 15.06.2002",
        "Updates the birthday of an existing contact. "
        "The new date must be in DD.MM.YYYY format.",
    ),
    "del-birthday": (
        "del-birthday <name>",
        "del-birthday Peter",
        "Removes the birthday from a contact without " "deleting the contact itself.",
    ),
    "birthdays": (
        "birthdays [days]",
        "birthdays 30",
        "Displays upcoming birthdays within the specified "
        "number of calendar days, including today. "
        "The default period is 7 days. The number of days "
        "must be a positive integer. Weekend birthdays "
        "are displayed on their actual dates.",
    ),
    # Address management
    "add-address": (
        "add-address <name> <address>",
        "add-address Peter Baker Street 12",
        "Assigns an address to an existing contact. "
        "The address may contain multiple words. "
        "If an address already exists, asks for confirmation "
        "before replacing it.",
    ),
    "show-address": (
        "show-address <name>",
        "show-address Peter",
        "Displays the saved address of the specified contact.",
    ),
    "change-address": (
        "change-address <name> <new-address>",
        "change-address Peter Oxford Street 15",
        "Replaces the current address of an existing contact "
        "with the provided address.",
    ),
    "del-address": (
        "del-address <name>",
        "del-address Peter",
        "Removes the address from a contact without " "deleting the contact itself.",
    ),
    "show-all-addresses": (
        "show-all-addresses",
        "show-all-addresses",
        "Displays the names and addresses of all contacts "
        "that have a saved address. Contacts without "
        "an address are excluded.",
    ),
    # Email management
    "add-email": (
        "add-email <name> <email>",
        "add-email Peter peter@example.com",
        "Assigns an email address to an existing contact. "
        "If an email already exists, asks for confirmation "
        "before replacing it.",
    ),
    "change-email": (
        "change-email <name> <email>",
        "change-email Peter new@example.com",
        "Updates the email address of an existing contact. "
        "The new email must have a valid format.",
    ),
    "show-email": (
        "show-email <name>",
        "show-email Peter",
        "Displays the saved email address of " "the specified contact.",
    ),
    "del-email": (
        "del-email <name>",
        "del-email Peter",
        "Removes the email address from a contact "
        "without deleting the contact itself.",
    ),
    # Note management
    "add-note": (
        "add-note <name> <note>",
        "add-note Peter Call on Monday",
        "Creates a new text note associated with an "
        "existing contact. Notes may contain multiple words.",
    ),
    "edit-note": (
        "edit-note <name> <old note> | <new note>",
        "edit-note Peter Call on Monday | Call on Friday",
        "Updates an existing note associated with a contact. "
        "Provide the original note text and the replacement "
        "text separated by a vertical bar (|) with spaces.",
    ),
    "del-note": (
        "del-note <name> <note>",
        "del-note Peter Call on Monday",
        "Removes a specific note from a contact. "
        "Provide the contact name and the note text.",
    ),
    "search-notes": (
        "search-notes <query>",
        "search-notes Monday",
        "Searches saved notes using the provided text "
        "and displays matching notes with contact names.",
    ),
    # Tag management
    "add-tag": (
        "add-tag <name> <note text> | <tag>",
        "add-tag Peter Call on Monday | work",
        "Assigns a tag to an existing note to help organize "
        "and categorize notes. Separate the note text "
        "and tag using a vertical bar (|) with spaces.",
    ),
    "del-tag": (
        "del-tag <name> <note text> | <tag>",
        "del-tag Peter Call on Monday | work",
        "Removes a specific tag from an existing note "
        "without deleting the note itself.",
    ),
    "search-tags": (
        "search-tags <tag>",
        "search-tags work",
        "Searches notes across all contacts by the "
        "specified tag. Displays matching notes, "
        "contact names and tags.",
    ),
    "sort-tags": (
        "sort-tags",
        "sort-tags",
        "Displays notes organized by their tags, "
        "including contact names, note text and tags.",
    ),
    # Exit commands
    "close": (
        "close",
        "close",
        "Closes the assistant and saves the address book " "for future sessions.",
    ),
    "exit": (
        "exit",
        "exit",
        "Closes the assistant and saves the address book. "
        "Works as an alternative to the close command.",
    ),
}
