import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Intelligent Mapping Generator',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        AI-powered field mapping generation for ISO 20022 messages. Automatically
        analyze and generate field mappings between different payment message formats
        with confidence scoring and validation.
      </>
    ),
  },
  {
    title: 'XML Sanitization',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Clean and validate ISO 20022 XML messages with comprehensive sanitization.
        Supports multiple message types including <code>pain.001</code>, <code>pacs.008</code>,
        and CBPR+ standards.
      </>
    ),
  },
  {
    title: 'CSV Parser',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Python-powered CSV parsing and transformation. Auto-detect encodings, validate
        structures, extract schemas, and transform data with ease. Perfect for
        financial data ingestion and processing workflows.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
