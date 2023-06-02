from typing import Sequence
from pydantic import BaseModel


class YouGileDeadline(BaseModel):
    """ Модель дэдлайна YouGile. """
    deadline: int
    startDate: int | None
    withTime: bool | None


class YouGileTimeTracking(BaseModel):
    """ Модель стикера таймтрекинга YouGile. """
    plan: int
    work: int


class YouGileCheckListItems(BaseModel):
    """ Модель объектов чеклиста YouGile. """
    title: str
    isCompleted: bool


class YouGileCheckList(BaseModel):
    """ Модель чеклиста YouGile. """
    title: str
    items: list[YouGileCheckListItems]


class YouGileStopwatch(BaseModel):
    """ Модель секундомера YouGile. """
    running: bool
    seconds: int
    atMoment: int


class YouGileTimer(BaseModel):
    """ Модель таймера YouGile. """
    seconds: int
    since: int
    running: bool


class YouGileTask(BaseModel):
    """ Модель такски YouFile. """
    id: str
    deleted: bool | None
    title: str
    timestamp: int
    columnId: str | None
    description: str | None
    archived: bool | None
    archivedTimestamp: int | None
    completed: bool | None
    completedTimestamp: int | None
    subtasks: list[str] | None
    # Кто додумался писать в доке list [str], а придти может и просто str?
    assigned: list[str] | str | None
    createdBy: str | None
    deadline: YouGileDeadline | None
    timeTracking: YouGileTimeTracking | None
    checklists: YouGileCheckList | None
    stickers: dict | None
    stopwatch: YouGileStopwatch | None
    timer: YouGileTimer | None


class YouGileUser(BaseModel):
    """ Модель YouGile пользователя. """
    id: str
    email: str
    isAdmin: bool | None
    realName: str
    status: str
    lastActivity: int


class YouGileTaskUpdate(BaseModel):
    """ Модель обновы такси YouGile. """
    event: str
    payload: YouGileTask
    fromUserId: str


class BotCommand(BaseModel):
    """ Модель команд бота. """
    command: str
    description: str


class BotCommandList(BaseModel):
    """ Модель списка команд бота. """
    __root__: Sequence[BotCommand]


class User(BaseModel):
    '''
        Модель пользователя.
    '''
    id: int
    is_bot: str
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    is_premium: bool | None
    added_to_attachment_menu: bool | None
    can_join_groups: bool | None
    can_read_all_group_messages: bool | None
    supports_inline_queries: bool | None


class ChatPhoto(BaseModel):
    '''
        Модель фотографии чата.
    '''
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatPermissions(BaseModel):
    '''
        Модель разрешений чата.
    '''
    can_send_messages: bool | None
    can_send_audios: bool | None
    can_send_documents: bool | None
    can_send_photos: bool | None
    can_send_videos: bool | None
    can_send_video_notes: bool | None
    can_send_voice_notes: bool | None
    can_send_polls: bool | None
    can_send_other_messages: bool | None
    can_add_web_page_previews: bool | None
    can_change_info: bool | None
    can_invite_users: bool | None
    can_pin_messages: bool | None
    can_manage_topics: bool | None


class Location(BaseModel):
    '''
        Модель локации.
    '''
    longitude: float
    latitude: float
    horizontal_accuracy: float | None
    live_period: int | None
    heading: int | None
    proximity_alert_radius: int | None


class ChatLocation(BaseModel):
    '''
        Модель локации чата.
    '''
    location: Location
    address: str


class Chat(BaseModel):
    '''
        Модель чата.
    '''
    id: int
    type: str
    title: str | None
    username: str | None
    first_name: str | None
    last_name: str | None
    is_forum: bool | None
    photo: ChatPhoto | None
    active_usernames: list[str] | None
    emoji_status_custom_emoji_id: str | None
    bio: str | None
    has_private_forwards: bool | None
    has_restricted_voice_and_video_messages: bool | None
    join_to_send_messages: bool | None
    join_by_request: bool | None
    description: str | None
    invite_link: str | None
    pinned_message: dict | None
    permissions: ChatPermissions | None
    slow_mode_delay: int | None
    message_auto_delete_time: int | None
    has_aggressive_anti_spam_enabled: bool | None
    has_hidden_members: bool | None
    has_protected_content: bool | None
    sticker_set_name: str | None
    can_set_sticker_set: bool | None
    linked_chat_id: int | None
    location: ChatLocation | None


class MessageEntity(BaseModel):
    '''
        Модель сущности сообщения.
    '''
    type: str
    offset: int
    length: int
    url: str | None
    user: User | None
    language: str | None
    custom_emoji_id: str | None


class PhotoSize(BaseModel):
    '''
        Модель размеров картинок/файлов/стикеров.
    '''
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int | None


class Animation(BaseModel):
    '''
        Модель анимационного файла (GIF или H.264/MPEG-4 AVC без звука).
    '''
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: PhotoSize | None
    file_name: str | None
    mime_type: str | None
    file_size: int | None


class Audio(BaseModel):
    '''
        Модель аудиофайлов.
    '''
    file_id: str
    file_unique_id: str
    duration: int
    performer: str | None
    title: str | None
    file_name: str | None
    mime_type: str | None
    file_size: int | None
    thumbnail: PhotoSize | None


class Document(BaseModel):
    '''
        Модель документа.
    '''
    file_id: str
    file_unique_id: str
    thumbnail: PhotoSize | None
    file_name: str | None
    mime_type: str | None
    file_size: int | None


class File(BaseModel):
    '''
        Модель, файла, готового к скачиванию.
        Ссылка: (https://api.telegram.org/file/bot<token>/<file_path>)
    '''
    file_id: str
    file_unique_id: str
    file_size: int | None
    file_path: str | None


class Sticker(BaseModel):
    '''
        Модель стикера.
    '''
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: PhotoSize | None
    emoji: str | None
    set_name: str | None
    premium_animation: File | None
    mask_position: dict | None
    custom_emoji_id: str | None
    needs_repainting: bool | None
    file_size: int | None


class Video(BaseModel):
    '''
        Модель видео файла.
    '''
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: PhotoSize | None
    file_name: str | None
    mime_type: str | None
    file_size: int | None


class VideoNote(BaseModel):
    '''
        Модель кружка (видео-сообщение).
    '''
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: PhotoSize | None
    file_size: int | None


class Voice(BaseModel):
    '''
        Модель голосового сообщения.
    '''
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str | None
    file_size: int | None


class Contact(BaseModel):
    '''
        Модель телефонного контакта.
    '''
    phone_number: str
    first_name: str
    last_name: str | None
    user_id: int | None
    vcard: str | None


class Dice(BaseModel):
    '''
        Модель эмодзи со случайным значением.
    '''
    emoji: str
    value: int


class WebAppData(BaseModel):
    '''
        Модель Web App.
    '''
    data: str
    button_text: str


class InlineKeyboardButton(BaseModel):
    '''
        Модель кнопок inline-клавиатуры.
    '''
    text: str
    url: str | None
    callback_data: str | None
    web_app: dict | None
    login_url: dict | None
    switch_inline_query: str | None
    switch_inline_query_current_chat: str | None
    switch_inline_query_chosen_chat: dict | None
    callback_game: dict | None
    pay: bool | None


class InlineKeyboardMarkup(BaseModel):
    '''
        Модель inline-клавиатуры.
    '''
    inline_keyboard: list[list[InlineKeyboardButton]]


class InlineQuery(BaseModel):
    '''
        Модель входящего inline-query.
    '''
    id: str
    from_user: User
    query: str
    offset: str
    chat_type: str | None
    location: dict | None

    class Config:
        fields = {
            'from_user': 'from'
        }


class Message(BaseModel):
    '''
        Модель сообщения.
    '''
    message_id: int
    message_thread_id: int | None
    from_user: User | None
    sender_chat: Chat | None
    date: int
    chat: Chat
    forward_from: User | None
    forward_from_chat: Chat | None
    forward_from_message_id: int | None
    forward_signature: str | None
    forward_sender_name: str | None
    forward_date: int | None
    is_topic_message: bool | None
    is_automatic_forward: bool | None
    reply_to_message: dict | None
    via_bot: User | None
    edit_date: str | None
    has_protected_content: bool | None
    media_group_id: str | None
    author_signature: str | None
    text: str | None
    entities: list[MessageEntity] | None
    animation: Animation | None
    audio: Audio | None
    document: Document | None
    photo: list[PhotoSize] | None
    sticker: Sticker | None
    video: Video | None
    video_note: VideoNote | None
    voice: Voice | None
    caption: str | None
    caption_entities: list[MessageEntity] | None
    has_media_spoiler: bool | None
    contact: Contact | None
    dice: Dice | None
    game: dict | None
    poll: dict | None
    venue: dict | None
    location: dict | None
    new_chat_members: list[User] | None
    left_chat_member: User | None
    new_chat_title: str | None
    new_chat_photo: list[PhotoSize] | None
    delete_chat_photo: bool | None
    group_chat_created: bool | None
    supergroup_chat_created: bool | None
    channel_chat_created: bool | None
    message_auto_delete_timer_changed: dict | None
    migrate_to_chat_id: int | None
    migrate_from_chat_id: int | None
    pinned_message: dict | None
    invoice: dict | None
    successful_payment: dict | None
    user_shared: dict | None
    chat_shared: dict | None
    connected_website: str | None
    write_access_allowed: dict | None
    passport_data: dict | None
    proximity_alert_triggered: dict | None
    forum_topic_created: dict | None
    forum_topic_edited: dict | None
    forum_topic_closed: dict | None
    forum_topic_reopened: dict | None
    general_forum_topic_hidden: dict | None
    general_forum_topic_unhidden: dict | None
    video_chat_scheduled: dict | None
    video_chat_started: dict | None
    video_chat_ended: dict | None
    video_chat_participants_invited: dict | None
    web_app_data: WebAppData | None
    reply_markup: InlineKeyboardMarkup | None

    class Config:
        fields = {
            'from_user': 'from'
        }


class CallbackQuery(BaseModel):
    id: str
    from_user: User
    message: Message | None
    inline_message_id: str | None
    chat_instance: str
    data: str | None
    game_short_name: str | None

    class Config:
        fields = {
            'from_user': 'from'
        }


class TelegramUpdate(BaseModel):
    '''
        Модель обновления для вебхук.
    '''
    update_id: int
    message: Message | None
    edited_message: Message | None
    channel_post: Message | None
    edited_channel_post: Message | None
    inline_query: InlineQuery | None
    chosen_inline_result: dict | None
    callback_query: CallbackQuery | None
    shipping_query: dict | None
    pre_checkout_query: dict | None
    poll: dict | None
    poll_answer: dict | None
    my_chat_member: dict | None
    chat_member: dict | None
    chat_join_request: dict | None
