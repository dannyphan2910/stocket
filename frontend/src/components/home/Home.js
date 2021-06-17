import { Col, Row } from 'antd';
import React, { useState } from 'react';
import GeneralLayout from '../shared/GeneralLayout';
import NewsCard from './NewsCard';
import PortfolioCard from './PortfolioCard';
import PortfolioDetailsCard from './PortfolioDetailsCard';
import SuggestionCard from './SuggestionCard';

function Home() {
    const [portfolio, setPortfolio] = useState({});

    return (
        <GeneralLayout componentName="">
            <Row gutter={[25, 25]}>
                <Col span={20}>
                    <PortfolioCard />
                </Col>
                <Col flex="auto">
                    <PortfolioDetailsCard />
                </Col>
            </Row>
            <Row style={{ marginTop: '50px' }}>
                <Col span={24}>
                    <NewsCard />
                </Col>
            </Row>
            <Row style={{ marginTop: '50px' }}>
                <Col span={24}>
                    <SuggestionCard />
                </Col>
            </Row>
        </GeneralLayout>
    )
}

export default Home;