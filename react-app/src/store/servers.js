//need to change
const SET_ALL_SERVERS = "servers/SetAllServers";
const SET_USER_SERVERS = "servers/SetUserServers";
const ADD_USER_SERVER = "servers/AddUserServer";
const REMOVE_USER_SERVER = "servers/RemoveUserServer";
const UPDATE_USER_SERVERS = "servers/UpdateOwnedServers";
const SET_SELECTED_SERVER = "currentServer/SetSelectedServer";
const CLEAR_SELECTED_SERVER = "currentServer/ClearSelectedServer";
const UPDATE_CURRENT_SERVER = "currentServer/UpdateSelectedServer";
const ADD_MEMBER_TO_SERVER = "currentServer/AddMember";
const REMOVE_MEMBER_FROM_SERVER = "currentServer/RemoveMember";

// adds servers to the store
export const setAllServers = (servers) => {
  return { type: SET_ALL_SERVERS, servers };
};

export const getAllServers = () => async (dispatch) => {
    const res = await fetch("/api/servers");
    const servers = await res.json();
  
    dispatch(setAllServers(servers.servers));
    return servers.servers;
  };


// sets servers the user belongs in the store
export const setUserServers = (servers) => {
    return { type: SET_USER_SERVERS, servers };
  };

export const addUserServer = (server) => {
    return { type: ADD_USER_SERVER, server };
  };
export const joinUserServer = (serverId, userId) => async (dispatch) => {
    const res = await fetch(`/api/servers/${serverId}/members`, {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ serverId, userId }),
    });
    const data = await res.json();
    dispatch(addUserServer(data.server));
    return data.server;
  };

  export const postUserServer = (formData) => async (dispatch) => {
      const res = await fetch("/api/servers/", {
        method: "POST",
        body: formData,
      });
      const newServer = await res.json();
    
      dispatch(addUserServer(newServer));
      return newServer;
    };


// remove a server the user joined in the store
export const removeUserServer = (serverId) => {
      return { type: REMOVE_USER_SERVER, serverId };
    };
    
// deletes the user from a server they joined
export const leaveUserServer = (serverId, membershipId) => async (dispatch) => {
    const res = await fetch(
      `/api/servers/${serverId}/members/${membershipId}`,
      {
        method: "DELETE",
      }
    );
    const data = await res.json();
    dispatch(removeUserServer(data.serverId));
  };

export const deleteServer = (serverId) => async (dispatch) => {
    await fetch(`/api/servers/${serverId}`, {
      method: "DELETE",
    });
    dispatch(removeUserServer(serverId));
  };



  export const setCurrentServer = (server) => {
    return { type: SET_SELECTED_SERVER, server };
  };
//   export const clearCurrentServer = () => {
//     return { type: CLEAR_CURRENT_SERVER };
//   };

export const getAServer = (serverId) => async (dispatch) => {
    const res = await fetch(`/api/servers/${serverId}`);
  
    const server = await res.json();
  
    dispatch(setCurrentServer(server));
    //dispatch(setChannels(server.channels));
  };



  export const updateCurrentServer = (server) => {
    return { type: UPDATE_CURRENT_SERVER, server };
  };

  export const updateUserServers = (server) => {
    return { type: UPDATE_USER_SERVERS, server };
  };

  export const putCurrentServer = (serverId, formData) => async (dispatch) => {
    const res = await fetch(`/api/servers/${serverId}`, {
      method: "PUT",
      body: formData,
    });
    const updatedServer = await res.json();
  
    dispatch(updateCurrentServer(updatedServer));
    dispatch(updateUserServers(updatedServer));
    // dispatch(setChannels(updatedServer.channels));
  
    // return updatedServer.picture;
  };

export const addMember = (serverId, member) => {
    return { type: ADD_MEMBER_TO_SERVER, serverId, member };
  };

export const removeMember = (serverId, memberId) => {
    return { type: REMOVE_MEMBER_FROM_SERVER, serverId, memberId };
  };

  const serversReducer = (
    state = {
      userServers: { server: null },
      allServers: { server: null },
      currentServer: {
        server: null,
      },
    },
    action
  ) => {
    let newState = { ...state };
    switch (action.type) {
    //   case CLEAR_ALL_SERVERS: {
    //     newState = {
    //       userServers: { server: null },
    //       allServers: { server: null },
    //       currentServer: {
    //         server: null,
    //       },
    //     };
    //     return newState;
    //   }
  
      case CLEAR_SELECTED_SERVER: {
        newState.currentServer = null;
        return newState;
      }
      case SET_ALL_SERVERS: {
        newState.allServers = action.servers;
        return newState;
      }
      case SET_USER_SERVERS: {
        newState.userServers = action.servers;
        return newState;
      }
  
      case UPDATE_USER_SERVERS: {
        newState.userServers[action.server.id] = action.server;
        return newState;
      }
  
      case ADD_USER_SERVER: {
        newState.userServers[action.server.id] = action.server;
        return newState;
      }
  
      case REMOVE_USER_SERVER: {
        delete newState.userServers[action.serverId];
        return newState;
      }
  
      case SET_SELECTED_SERVER: {
        newState.currentServer = action.server;
        return newState;
      }
  
      case UPDATE_CURRENT_SERVER: {
        newState.currentServer = action.server;
        return newState;
      }
  
      case ADD_MEMBER_TO_SERVER: {
        newState.currentServer.members[action.member.id] = action.member;
        return newState;
      }
  
      case REMOVE_MEMBER_FROM_SERVER: {
        delete newState.currentServer.members[action.memberId];
        return newState;
      }
  
      default:
        return state;
    }
  };
  
  export default serversReducer;
