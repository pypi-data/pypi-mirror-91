import numpy as np
from numpy.testing import assert_allclose, raises
from menpo.shape import PointCloud
from menpo.transform import (
    Affine,
    AlignmentAffine,
    Similarity,
    AlignmentSimilarity,
    Rotation,
    AlignmentRotation,
    Translation,
    AlignmentTranslation,
    UniformScale,
    AlignmentUniformScale,
)

# TODO check composition works correctly on all alignment methods


# AFFINE


def test_align_2d_affine():
    linear_component = np.array([[1, -6], [-3, 2]])
    translation_component = np.array([7, -8])
    h_matrix = np.eye(3, 3)
    h_matrix[:-1, :-1] = linear_component
    h_matrix[:-1, -1] = translation_component
    affine = Affine(h_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = affine.apply(source)
    # estimate the transform from source and target
    estimate = AlignmentAffine(source, target)
    # check the estimates is correct
    assert_allclose(affine.h_matrix, estimate.h_matrix, atol=1e-3, rtol=1e-3)


def test_align_2d_affine_compose_target():
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = UniformScale(2.0, n_dims=2).apply(source)
    original_estimate = AlignmentAffine(source, target)
    new_estimate = original_estimate.copy()
    new_estimate.compose_after_from_vector_inplace(np.array([0, 0, 0, 0, 1, 1.0]))
    estimate_target = new_estimate.target

    correct_target = original_estimate.compose_after(Translation([1, 1.0])).apply(
        source
    )

    assert_allclose(estimate_target.points, correct_target.points)


def test_align_2d_affine_set_target():
    linear_component = np.array([[1, -6], [-3, 2]])
    translation_component = np.array([7, -8])
    h_matrix = np.eye(3, 3)
    h_matrix[:-1, :-1] = linear_component
    h_matrix[:-1, -1] = translation_component
    affine = Affine(h_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = affine.apply(source)
    # estimate the transform from source and source
    estimate = AlignmentAffine(source, source)
    # and set the target
    estimate.set_target(target)
    # check the estimates is correct
    assert_allclose(affine.h_matrix, estimate.h_matrix, atol=1e-3, rtol=1e-3)


def test_align_2d_affine_as_non_alignment():
    linear_component = np.array([[1, -6], [-3, 2]])
    translation_component = np.array([7, -8])
    h_matrix = np.eye(3, 3)
    h_matrix[:-1, :-1] = linear_component
    h_matrix[:-1, -1] = translation_component
    affine = Affine(h_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = affine.apply(source)
    # estimate the transform from source and source
    estimate = AlignmentAffine(source, source)
    # and set the h_matrix
    non_align = estimate.as_non_alignment()
    # check the estimates is correct
    assert_allclose(non_align.h_matrix, estimate.h_matrix)
    assert type(non_align) == Affine


# TODO check from_vector, from_vector_inplace works correctly


# SIMILARITY


def test_align_2d_similarity():
    linear_component = np.array([[2, -6], [6, 2]])
    translation_component = np.array([7, -8])
    h_matrix = np.eye(3, 3)
    h_matrix[:-1, :-1] = linear_component
    h_matrix[:-1, -1] = translation_component
    similarity = Similarity(h_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = similarity.apply(source)
    # estimate the transform from source and target
    estimate = AlignmentSimilarity(source, target)
    # check the estimates is correct
    assert_allclose(similarity.h_matrix, estimate.h_matrix)


def test_align_2d_similarity_set_target():
    linear_component = np.array([[2, -6], [6, 2]])
    translation_component = np.array([7, -8])
    h_matrix = np.eye(3, 3)
    h_matrix[:-1, :-1] = linear_component
    h_matrix[:-1, -1] = translation_component
    similarity = Similarity(h_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = similarity.apply(source)
    # estimate the transform from source to source
    estimate = AlignmentSimilarity(source, source, allow_mirror=True)
    # and set the target
    estimate.set_target(target)
    # check the estimates is correct
    assert_allclose(similarity.h_matrix, estimate.h_matrix)


# ROTATION


def test_align_2d_rotation():
    rotation_matrix = np.array([[0, 1], [-1, 0]])
    rotation = Rotation(rotation_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = rotation.apply(source)
    # estimate the transform from source and target
    estimate = AlignmentRotation(source, target)
    # check the estimates is correct
    assert_allclose(rotation.h_matrix, estimate.h_matrix, atol=1e-14)


def test_align_2d_rotation_allow_mirror():
    s_init = PointCloud(np.array([[-1.0, 1.0], [1.0, 1.0], [1.0, -1.0], [-1.0, -1.0]]))
    s_trg = PointCloud(np.array([[1.0, -1.0], [1.0, 1.0], [-1.0, 1.0], [-1.0, -1.0]]))
    # estimate the transform from source and target with mirroring allowed
    tr = AlignmentRotation(s_init, s_trg, allow_mirror=True)
    s_final = tr.apply(s_init)
    assert_allclose(s_final.points, s_trg.points, atol=1e-14)
    # estimate the transform from source and target with mirroring allowed
    tr = AlignmentRotation(s_init, s_trg, allow_mirror=False)
    s_final = tr.apply(s_init)
    assert_allclose(
        s_final.points,
        np.array([[-1.0, -1.0], [-1.0, 1.0], [1.0, 1.0], [1.0, -1.0]]),
        atol=1e-14,
    )


def test_align_2d_rotation_set_target():
    rotation_matrix = np.array([[0, 1], [-1, 0]])
    rotation = Rotation(rotation_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = rotation.apply(source)
    # estimate the transform from source and source
    estimate = AlignmentRotation(source, source)
    # and set the target
    estimate.set_target(target)
    # check the estimates is correct
    assert_allclose(rotation.h_matrix, estimate.h_matrix, atol=1e-14)


def test_align_2d_rotation_set_rotation_matrix():
    rotation_matrix = np.array([[0, 1], [-1, 0]])
    rotation = Rotation(rotation_matrix)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = rotation.apply(source)
    # estimate the transform from source and source
    estimate = AlignmentRotation(source, source)
    # and set the target
    estimate.set_rotation_matrix(rotation.rotation_matrix)
    # check the estimates is correct
    assert_allclose(target.points, estimate.target.points, atol=1e-14)


# UNIFORM SCALE


def test_align_2d_uniform_scale():
    scale = UniformScale(2.5, 2)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = scale.apply(source)
    # estimate the transform from source and target
    estimate = AlignmentUniformScale(source, target)
    # check the estimates is correct
    assert_allclose(scale.h_matrix, estimate.h_matrix)


def test_align_2d_uniform_scale_set_target():
    scale = UniformScale(2.5, 2)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = scale.apply(source)
    # estimate the transform from source and source
    estimate = AlignmentUniformScale(source, source)
    # and set the target
    estimate.set_target(target)
    # check the estimates is correct
    assert_allclose(scale.h_matrix, estimate.h_matrix)


# TRANSLATION


def test_align_2d_translation():
    t_vec = np.array([1, 2])
    translation = Translation(t_vec)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = translation.apply(source)
    # estimate the transform from source and target
    estimate = AlignmentTranslation(source, target)
    # check the estimates is correct
    assert_allclose(translation.h_matrix, estimate.h_matrix)


def test_align_2d_translation_set_target():
    t_vec = np.array([1, 2])
    translation = Translation(t_vec)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = translation.apply(source)
    # estimate the transform from source to source..
    estimate = AlignmentTranslation(source, source)
    # and change the target.
    estimate.set_target(target)
    # check the estimates is correct
    assert_allclose(translation.h_matrix, estimate.h_matrix)


def test_align_2d_translation_from_vector_inplace():
    t_vec = np.array([1, 2])
    translation = Translation(t_vec)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = translation.apply(source)
    # estimate the transform from source to source..
    estimate = AlignmentTranslation(source, source)
    # and update from_vector
    estimate._from_vector_inplace(t_vec)
    # check the estimates is correct
    assert_allclose(target.points, estimate.target.points)


def test_align_2d_translation_from_vector():
    t_vec = np.array([1, 2])
    translation = Translation(t_vec)
    source = PointCloud(np.array([[0, 1], [1, 1], [-1, -5], [3, -5]]))
    target = translation.apply(source)
    # estimate the transform from source to source..
    estimate = AlignmentTranslation(source, source)
    # and update from_vector
    new_est = estimate.from_vector(t_vec)
    # check the original is unchanged
    assert_allclose(estimate.source.points, source.points)
    assert_allclose(estimate.target.points, source.points)
    # check the new estimate has the source and target correct
    assert_allclose(new_est.source.points, source.points)
    assert_allclose(new_est.target.points, target.points)
