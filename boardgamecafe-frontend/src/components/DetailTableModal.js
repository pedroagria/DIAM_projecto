import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";
import DetailTableForm from "./DetailTableForm";

class DetailTableModal extends Component {
    state = {
        modal: false
    };

    toggle = () => {
        this.setState(previous => ({
            modal: !previous.modal
        }));
    };

    render(){
        var title = "Table Detail";
        var button = <Button onClick={this.toggle} color="warning">Detail</Button>;
        return(
            <Fragment>
                {button}
                <Modal isOpen={this.state.modal} toggle={this.toggle}>
                    <ModalHeader toggle={this.toggle}>{title}</ModalHeader>
                    <ModalBody>
                        <DetailTableForm
                            resetState={this.props.resetState}
                            toggle={this.toggle}
                            table={this.props.table}
                        />
                    </ModalBody>
                </Modal>
            </Fragment>
        );
    }
}

export default DetailTableModal;