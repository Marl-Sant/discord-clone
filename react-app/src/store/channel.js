// const CLEAR_CHANNELS_STORE = "logout/CLEAR CHANNELS";
const SET_SERVER_CHANNELS = "channels/setChannels";
const SET_USER_DM_CHANNELS = "dms/setsUserDmChannels";
const ADD_CHANNEL_TO_SERVER = "channels/AddChannel";
const UPDATE_CHANNEL_ON_SERVER = "channels/UpdateChannel";
const REMOVE_CHANNEL_FROM_SERVER = "channels/RemoveChannel";
const SET_CURRENT_CHANNEL = "currentChannel/SetCurrentChannel";
// const CLEAR_CURRENT_CHANNEL = "currentChannel/Clear";
const ADD_CHANNEL_MESSAGE = "currentChannel/AddMessage";
const UPDATE_CHANNEL_MESSAGE = "currentChannel/UpdateMessage";
const REMOVE_CHANNEL_MESSAGE = "currentChannel/RemoveMessage";

// set channels in the store
export const setChannels = (channels) => {
    return { type: SET_SERVER_CHANNELS, channels };
};

// add a new channel to the store
export const addChannel = (serverId, channel) => {
    return { type: ADD_CHANNEL_TO_SERVER, serverId, channel };
};

// create a new channel and set it in the store
export const postChannel = (channel) => async (dispatch) => {
    const res = await fetch(`/api/servers/${channel.serverId}/channels`, {
        method: "POST",
        body: JSON.stringify(channel),
    });

    const newChannel = await res.json();

    dispatch(addChannel(newChannel.serverId, newChannel));
    dispatch(setCurrentChannel(newChannel));
    return newChannel;
};

//edit a channel in a server
export const updateChannel = (serverId, channel) => {
    return { type: UPDATE_CHANNEL_ON_SERVER, serverId, channel };
};

export const putChannel = (channel) => async (dispatch) => {
    const res = await fetch(
        `/api/servers/${channel.serverId}/channels/${channel.id}`,
        {
            method: "PUT",
            body: JSON.stringify(channel),
        }
    );

    const updatedChannel = await res.json();

    dispatch(updateChannel(updatedChannel.serverId, updatedChannel));
};

//remove a channel from a server
export const removeChanel = (serverId, channelId) => {
    return { type: REMOVE_CHANNEL_FROM_SERVER, serverId, channelId };
};

export const deleteChannel = (serverId, channelId) => async (dispatch) => {
    const res = await fetch(
        `/api/servers/${serverId}/channels/${channelId}`,
        {
            method: "DELETE",
        }
    );
    const deletedChannel = await res.json();
    dispatch(removeChanel(serverId, deletedChannel.channelId));
};

//set the selected channel to the current channel in the store
export const setCurrentChannel = (channel) => {
    return { type: SET_CURRENT_CHANNEL, channel };
};

export const getAChannel = (channelId) => async (dispatch) => {
    const res = await fetch(`/api/channels/${channelId}`);

    const channel = await res.json();
    dispatch(setCurrentChannel(channel));
    return channel;
};

// export const clearCurrentChannel = () => {
//     return { type: CLEAR_CURRENT_CHANNEL };
//   };

//add new message to the store
export const addChannelMessage = (message) => {
    return { type: ADD_CHANNEL_MESSAGE, message };
};

export const postMessage = (channelId, formData) => async (dispatch) => {
    const res = await fetch(`/api/channels/${channelId}/messages`, {
        method: "POST",
        body: formData,
    });

    const newMessage = await res.json();

    dispatch(addChannelMessage(newMessage));
    return newMessage;
};

//delete a message from the store

export const removeChannelMessage = (messageId) => {
    return { type: REMOVE_CHANNEL_MESSAGE, messageId };
};

export const deleteChannelMessage =
    (channelId, messageId) => async (dispatch) => {
        const res = await fetch(
            `/api/channels/${channelId}/messages/${messageId}`,
            {
                method: "DELETE",
            }
        );
        const deletedMessage = await res.json();
        dispatch(removeChannelMessage(deletedMessage.messageId));
    };

const channelsReducer = (
    state = {
        channels: {},
        currentChannel: { channel: null, pins: {} },
        userDmChannels: {},
        dmCurrentChannel: {},
    },
    action
) => {
    let newState = { ...state };
    switch (action.type) {
        // case CLEAR_CHANNELS_STORE: {
        //     newState = {
        //         channels: {},
        //         currentChannel: { channel: null, pins: {} },
        //         userDmChannels: {},
        //         dmCurrentChannel: {},
        //     };
        //     return newState;
        // }

        case SET_USER_DM_CHANNELS: {
            newState.userDmChannels = action.dmRooms;
            return newState;
        }

        case ADD_CHANNEL_TO_SERVER: {
            newState.channels[action.channel.id] = action.channel;
            return newState;
        }

        case UPDATE_CHANNEL_ON_SERVER: {
            newState.channels[action.channel.id] = action.channel;
            newState.currentChannel = action.channel;
            return newState;
        }

        case REMOVE_CHANNEL_FROM_SERVER: {
            delete newState.channels[action.channelId];
            return newState;
        }

        case SET_SERVER_CHANNELS: {
            newState.channels = action.channels;
            return newState;
        }

        case SET_CURRENT_CHANNEL: {
            newState.currentChannel = action.channel;
            return newState;
        }

        // case CLEAR_CURRENT_CHANNEL: {
        //     newState.currentChannel = null;
        //     return newState;
        // }

        case ADD_CHANNEL_MESSAGE: {
            newState.currentChannel.messages[action.message.id] = action.message;
            return newState;
        }

        case UPDATE_CHANNEL_MESSAGE: {
            newState.currentChannel.messages[action.message.id] = action.message;
            return newState;
        }

        case REMOVE_CHANNEL_MESSAGE: {
            delete newState.currentChannel.messages[action.messageId];
            return newState;
        }
        default:
            return state;
    }
};

export default channelsReducer;
