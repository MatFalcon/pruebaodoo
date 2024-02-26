/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            required: true,
            shape: {
                id: { required: true },
                description: { required: true },
                completed: { required: true },
            },
        },
        delete: { required: true, },
    };

    setup() {
        this.state = useState({});
    }

    toggleState() {
        this.props.todo.completed = !this.props.todo.completed;
    }

    delete() {
        this.props.delete(this.props.todo.id);
    }
}
