import { List } from 'antd';
import React from 'react';
import GeneralCard from '../shared/GeneralCard';

function PortfolioDetailsCard(props) {
    const availableTickers = [
        {
            title: 'Ant Design Title 1',
        },
        {
            title: 'Ant Design Title 2',
        },
        {
            title: 'Ant Design Title 3',
        },
        {
            title: 'Ant Design Title 4',
        },
        {
            title: 'Ant Design Title 5',
        },
        {
            title: 'Ant Design Title 6',
        },
    ];

    console.log(availableTickers);

    return (
        <GeneralCard style={{ minHeight: '650px', height: '85vh', overflow: 'auto' }}>
            <List
                itemLayout="horizontal"
                dataSource={availableTickers}
                renderItem={item => (
                    <List.Item>
                        <List.Item.Meta
                            title={<a href="https://ant.design" style={{ color: 'white' }}>{item.title}</a>}
                            description={<p style={{ color: 'white' }}>"Ant Design, a design language for background applications, is refined by Ant UED Team"</p>}
                        />
                    </List.Item>
                )}
            />
        </GeneralCard>
    );
}

export default PortfolioDetailsCard;