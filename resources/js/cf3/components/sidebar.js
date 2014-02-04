define(['react', 'underscore', 'components/glyphicon'], function (React, _, Glyphicon) {

    var SidebarListItem = React.createClass({
        handleClick: function(e) {
            e.preventDefault();
            this.props.onClick(this.props.id);
        },
        render: function() {
            var icon = this.props.icon ? Glyphicon({name: this.props.icon}) : null;

            return React.DOM.li(
                {className: this.props.active ? 'active' : ''}, 
                React.DOM.a(
                    {
                        href: url_root + this.props.id,
                        onClick: this.handleClick
                    },
                    icon,
                    this.props.text
                ),
                this.props.children
            );
        }
    });

    var SidebarSubmenu = React.createClass({
        render: function() {
            return React.DOM.ul({}, _.map(this.props.items, function(menu_item, key) {
                console.log(key);
                return SidebarListItem({
                    text: menu_item.text,
                    active: false
                });
            }));
        }
    });

    var Sidebar = React.createClass({
        onClick: function(clicked) {
            this.props.onSelect(clicked);
        },
        render: function() {
            var items = _.map(this.props.items, function(item, id) {
                return SidebarListItem({
                    icon: item.icon, 
                    active: id == this.props.active,
                    onClick: this.onClick,
                    text: item.text,
                    id: id
                }, SidebarSubmenu({items: item.submenu}));
            }.bind(this));
            return React.DOM.div({id: 'sidebar'}, React.DOM.ul({}, items));
        }
    });

    return Sidebar;
});
