### JavaDoc — Java Classes

Add or update Javadoc on changed Controller methods, Service methods, and Entities.

```java
/**
 * Submits user feedback.
 *
 * @param request the validated feedback request containing message and rating
 * @return the created feedback record with generated ID and timestamp
 * @throws ConstraintViolationException if request validation fails
 */
```

For entities, document non-obvious fields:

```java
/**
 * Numeric rating from 1 (poor) to 5 (excellent).
 * Validated at persistence layer — cannot be null or outside range.
 */
@Column(nullable = false)
private Integer rating;
```
