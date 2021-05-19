import React from 'react';
import { Card } from 'antd';
import './GeneralCard.css'

function GeneralCard(props) {
    const { children, style } = props;

    return (
        <Card className='styled-card' style={style}>
            {children}
        </Card>
    );
}

export default GeneralCard;