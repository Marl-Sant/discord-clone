import React, { useState } from "react";
import { Modal } from "../../context/Modal";
import CreateNewServer from ".";
import OpenModalButton from "../OpenModalButton";

const CreateNewServerModal = () => {

  return (
    <>
        <OpenModalButton
        buttonText="Create a Server"
        modalComponent={<CreateNewServer />}
      />

    </>
  );
};

export default CreateNewServerModal;
