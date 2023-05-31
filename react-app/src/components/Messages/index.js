import "./Messages.css";

const Messages = ({ messages }) => {

  return (
    <div className="messages">
      {messages?.map((message) => (
        <div className="message" key={message.id}>
          <div className="message_user">
            <img
              className="message_pfp"
              src={message.senderProfilePicture}
              alt="profilePicture"
            />
          </div>
          <div className="message_content">
            <h4 className="username">{message.senderUsername}</h4>
            <p>{message.content}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Messages;
