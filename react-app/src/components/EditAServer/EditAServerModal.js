import React, { useState } from "react";
import { Modal } from "../../context/Modal";
import EditAServer from ".";
import OpenModalButton from "../OpenModalButton";

const EditAServerModal = () => {
  return (
    <>
      {/* {showModal && (
        <Modal className="modal" onClose={() => setShowModal(false)}>
          <EditServer
            setShowModal={setShowModal}
            serversObj={serversObj}
            user={user}
          ></EditServer>
        </Modal>
      )} */}

        <OpenModalButton
        buttonText="Edit a Server"
        modalComponent={<EditAServer />}
      />
    </>
  );
};

export default EditAServerModal;
